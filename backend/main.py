import os
import sys
import cv2
import numpy as np
import io
import uuid
import json
import time
import logging
import psutil
from collections import deque
from fastapi import FastAPI, File, UploadFile, HTTPException, WebSocket, WebSocketDisconnect, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

# Ensure backend and project root directories are in sys.path to allow sibling imports
backend_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(backend_dir)
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Set up Structured Logging
os.makedirs("logs/sessions", exist_ok=True)
logging.basicConfig(
    level=logging.INFO if os.getenv("DEBUG_MODE") != "true" else logging.DEBUG,
    format='%(asctime)s | %(levelname)s | %(message)s'
)
logger = logging.getLogger("SHIELD")

# Global Metrics
class GlobalMetrics:
    def __init__(self):
        self.start_time = time.time()
        self.frames_processed = 0
        self.frames_dropped = 0
        self.latency_history = deque(maxlen=100)
        
    def add_latency(self, latency_ms):
        self.latency_history.append(latency_ms)
        self.frames_processed += 1
        
global_metrics = GlobalMetrics()
DEMO_MODE = os.getenv("DEMO_MODE", "false").lower() == "true"

from services.fusion_service import FusionService
from services.db_service import db_service
from services.seb_service import verify_seb_headers_http, verify_seb_headers_ws

app = FastAPI(title="SHIELD API", version="1.0.0")

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ensure local storage exists for serving
os.makedirs("local_storage/snapshots", exist_ok=True)
app.mount("/snapshots", StaticFiles(directory="local_storage/snapshots"), name="snapshots")

# Serve Flutter frontend
frontend_dir = os.path.abspath(os.path.join(project_root, "frontend/build/web"))
os.makedirs(frontend_dir, exist_ok=True) # Ensure it exists so FastAPI doesn't crash on startup
app.mount("/app", StaticFiles(directory=frontend_dir, html=True), name="frontend")
@app.get("/health")
async def health_check():
    process = psutil.Process(os.getpid())
    return {
        "status": "healthy",
        "service": "SHIELD",
        "camera": "WebSocket Connected",
        "decoder": "H.264 Ready",
        "mediapipe": "Loaded (VIDEO mode)",
        "models_loaded": True,
        "onnx_status": "Ready",
        "database": "Available",
        "memory_mb": process.memory_info().rss / 1024 / 1024,
        "uptime_s": time.time() - global_metrics.start_time
    }

@app.get("/metrics/debug")
async def get_metrics_debug():
    uptime = time.time() - global_metrics.start_time
    avg_latency = sum(global_metrics.latency_history) / len(global_metrics.latency_history) if global_metrics.latency_history else 0
    fps = global_metrics.frames_processed / uptime if uptime > 0 else 0
    return {
        "active_sessions": len(session_manager._sessions),
        "average_latency": avg_latency,
        "queue_depth": 0,
        "frames_processed": global_metrics.frames_processed,
        "frames_dropped": global_metrics.frames_dropped,
        "uptime": uptime,
        "backend_fps": fps
    }

from inference.session_manager import SessionManager

# Global Session Manager
session_manager = SessionManager()

from services.video_decoder import StreamingDecoder

@app.websocket("/ws/challenge")
async def websocket_challenge(websocket: WebSocket):
    """
    WebSocket endpoint for active challenge-response liveness streaming.
    Receives text messages (commands) and binary image data.
    """
    await websocket.accept()
    
    # SEB Cryptographic Trust Verification
    if not await verify_seb_headers_ws(websocket):
        await websocket.send_json({"type": "error", "message": "SEB Trust Verification Failed"})
        await websocket.close(code=1008)
        return
        
    client_host = websocket.client.host if websocket.client else "unknown"
    session_uuid = str(uuid.uuid4())
    logger.info(f"Client connected to Challenge WebSocket: {client_host} | Session: {session_uuid}")
    
    decoder = StreamingDecoder()
    session_fusion = FusionService()
    session_log_path = f"logs/sessions/session_{session_uuid}.jsonl"
    
    try:
        session = session_manager.create_session(client_id=client_host)
        challenge_session = session.challenge_session
    except RuntimeError as e:
        logger.error(f"Session error: {e}")
        await websocket.send_json({"type": "error", "message": str(e)})
        await websocket.close()
        return

    last_metadata = None

    try:
        while True:
            message = await websocket.receive()

            if "text" in message:
                try:
                    data = json.loads(message["text"])
                    if data.get("type") == "start_challenge":
                        challenge_session.start_current_challenge()
                        current = challenge_session.get_current_challenge()
                        await websocket.send_json({
                            "type": "challenge",
                            "action": current.value if current else None,
                            "timeout_s": challenge_session.timeout_per_challenge,
                            "index": challenge_session._current_index + 1,
                            "total": challenge_session.num_challenges
                        })
                        continue
                    
                    if "frameNumber" in data:
                        last_metadata = data
                except json.JSONDecodeError:
                    pass
                continue

            if "bytes" in message:
                print("FRAME_RECEIVED")
                data = message["bytes"]
                try:
                    frames = decoder.decode_chunk(data, metadata=last_metadata)
                    last_metadata = None
                    print("FRAME_DECODED")
                except Exception as e:
                    import traceback
                    print("FULL STACK TRACE")
                    traceback.print_exc()
                    logger.warning(f"Decode error: {e}")
                    await websocket.send_json({"type": "error", "message": f"Decode error: {e}"})
                    continue

                for decoded_frame in frames:
                    start_proc = time.time()
                    result = session_fusion.process_challenge_frame(
                        decoded_frame.image, 
                        challenge_session,
                        frame_number=decoded_frame.frame_number,
                        capture_timestamp=decoded_frame.capture_timestamp
                    )
                    raw_landmarks = result.pop("_raw_landmarks", None)
                    
                    frame_res = session.add_frame(decoded_frame.image, landmarks=raw_landmarks)
                    if not frame_res["accepted"]:
                        if frame_res.get("expired"):
                            logger.info("Session expired")
                            await websocket.send_json({"type": "error", "message": "Session expired"})
                            return
                        if frame_res.get("reason") == "identity_swap_detected":
                            logger.warning("Identity mismatch detected")
                            await websocket.send_json({"type": "error", "message": "Identity mismatch detected"})
                            return
                        continue
                
                    proc_latency = (time.time() - start_proc) * 1000
                    global_metrics.add_latency(proc_latency)
                    
                    # Log Session Data
                    with open(session_log_path, "a") as f:
                        log_entry = {
                            "timestamp": time.time(),
                            "session_id": session_uuid,
                            "frame_number": decoded_frame.metadata.get("frameNumber") if decoded_frame.metadata else None,
                            "latency_ms": proc_latency,
                            "verdict": result.get("verdict"),
                            "confidence": result.get("confidence")
                        }
                        f.write(json.dumps(log_entry) + "\n")
                    
                    # Demo Mode Visualization
                    if DEMO_MODE:
                        demo_img = decoded_frame.image.copy()
                        cv2.putText(demo_img, f"FPS: {global_metrics.frames_processed / (time.time() - global_metrics.start_time):.1f}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                        cv2.putText(demo_img, f"Latency: {proc_latency:.1f} ms", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                        cv2.putText(demo_img, f"Verdict: {result.get('verdict')}", (10, 110), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255) if result.get('verdict') != 'Live' else (0, 255, 0), 2)
                        
                        bbox = result.get("bbox")
                        if bbox:
                            x1, y1, x2, y2 = map(int, bbox)
                            cv2.rectangle(demo_img, (x1, y1), (x2, y2), (255, 0, 0), 2)
                            
                        if raw_landmarks:
                            for point in raw_landmarks:
                                x, y = int(point[0]), int(point[1])
                                cv2.circle(demo_img, (x, y), 2, (0, 255, 255), -1)
                        
                        if "challenge_info" in result:
                            act = result["challenge_info"].get("action")
                            det = result["challenge_info"].get("action_detected")
                            cv2.putText(demo_img, f"Challenge: {act}", (10, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
                            cv2.putText(demo_img, f"Detected: {det}", (10, 190), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
                            
                        cv2.imshow("SHIELD Demo Mode", demo_img)
                        cv2.waitKey(1)
                        
                    if "challenge_info" in result and "session_update" in result["challenge_info"]:
                        update = result["challenge_info"]["session_update"]
                        
                        if update.get("challenge_passed"):
                            await websocket.send_json({
                                "type": "challenge_result",
                                "action": result["challenge_info"]["action"],
                                "passed": True,
                                "next_action": update.get("next_challenge")
                            })
                            
                            if update.get("next_challenge"):
                                await websocket.send_json({
                                    "type": "challenge",
                                    "action": update.get("next_challenge"),
                                    "timeout_s": challenge_session.timeout_per_challenge,
                                    "index": challenge_session._current_index + 1,
                                    "total": challenge_session.num_challenges
                                })
                                
                        elif update.get("challenge_failed"):
                            await websocket.send_json({
                                "type": "challenge_result",
                                "action": result["challenge_info"]["action"],
                                "passed": False,
                                "next_action": update.get("next_challenge")
                            })
                            # If there's a next challenge after failure, re-issue it
                            if update.get("next_challenge") and not update.get("session_complete"):
                                current = challenge_session.get_current_challenge()
                                if current:
                                    challenge_session.start_current_challenge()
                                    await websocket.send_json({
                                        "type": "challenge",
                                        "action": current.value,
                                        "timeout_s": challenge_session.timeout_per_challenge,
                                        "index": challenge_session._current_index + 1,
                                        "total": challenge_session.num_challenges
                                    })
                            
                        if update.get("session_complete"):
                            # Send final verdict
                            final_res = session.get_final_result()
                            # Override verdict with the temporally validated one
                            result["verdict"] = final_res["verdict"]
                            result["temporal_valid"] = final_res["temporal_valid"]
                            result["challenge_score"] = final_res["challenge_score"]
                            await websocket.send_json(result)
                            return # End session
                    else:
                        # Normal frame update (can send partial progress if needed)
                        # For now, just send the frame result silently or omitted to save bandwidth
                        # We can send a generic verdict update
                        pass

    except WebSocketDisconnect:
        logger.info(f"Client disconnected from Challenge WS: {client_host} | Session: {session_uuid}")
    except Exception as e:
        logger.error(f"Challenge WS Error: {e}")
    finally:
        decoder.close()
        if DEMO_MODE:
            cv2.destroyAllWindows()
        # Cleanup the session to prevent memory leak and session limit issues
        if "session" in locals() and session.session_id in session_manager._sessions:
            try:
                del session_manager._sessions[session.session_id]
            except Exception as cleanup_err:
                logger.error(f"Error cleaning up challenge session: {cleanup_err}")
        try:
            await websocket.close()
        except:
            pass

@app.websocket("/ws/verify")
async def websocket_verify_passive(websocket: WebSocket):
    """
    WebSocket endpoint for passive liveness detection (no challenge prompts).
    Receives binary image frames and returns a fusion verdict per frame.
    """
    await websocket.accept()
    
    # SEB Cryptographic Trust Verification
    if not await verify_seb_headers_ws(websocket):
        await websocket.send_json({"error": "SEB Trust Verification Failed"})
        await websocket.close(code=1008)
        return
        
    client_host = websocket.client.host if websocket.client else "unknown"
    logger.info(f"Client connected to Passive Verify WebSocket: {client_host}")
    
    decoder = StreamingDecoder()
    session_fusion = FusionService()

    last_metadata = None

    try:
        while True:
            message = await websocket.receive()
            logger.info(f"WebSocket received message keys: {message.keys()}")

            if "text" in message:
                try:
                    data = json.loads(message["text"])
                    if "frameNumber" in data:
                        last_metadata = data
                except json.JSONDecodeError:
                    pass
                continue

            if "bytes" in message:
                print("FRAME_RECEIVED")
                data = message["bytes"]
                try:
                    frames = decoder.decode_chunk(data, metadata=last_metadata)
                    last_metadata = None
                    print("FRAME_DECODED")
                except Exception as e:
                    import traceback
                    print("FULL STACK TRACE")
                    traceback.print_exc()
                    logger.warning(f"Decode error: {e}")
                    await websocket.send_json({"error": f"Decode error: {e}"})
                    continue
                    
                for decoded_frame in frames:
                    result = session_fusion.process_frame(
                        decoded_frame.image,
                        frame_number=decoded_frame.frame_number,
                        capture_timestamp=decoded_frame.capture_timestamp
                    )
                    raw_landmarks = result.pop("_raw_landmarks", None)
                    
                    # Log the verdict to debug file
                    with open("logs/debug_verify.log", "a") as f:
                        f.write(json.dumps({
                            "timestamp": time.time(),
                            "verdict": result.get("verdict"),
                            "confidence": result.get("confidence"),
                            "details": result.get("details")
                        }) + "\\n")
                    
                    # Demo Mode Visualization
                    if DEMO_MODE:
                        demo_img = decoded_frame.image.copy()
                        cv2.putText(demo_img, f"Verdict: {result.get('verdict')}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255) if result.get('verdict') != 'Live' else (0, 255, 0), 2)
                        
                        bbox = result.get("bbox")
                        if bbox:
                            x1, y1, x2, y2 = map(int, bbox)
                            cv2.rectangle(demo_img, (x1, y1), (x2, y2), (255, 0, 0), 2)
                            
                        if raw_landmarks:
                            for point in raw_landmarks:
                                x, y = int(point[0]), int(point[1])
                                cv2.circle(demo_img, (x, y), 2, (0, 255, 255), -1)
                            
                        cv2.imshow("SHIELD Demo Mode", demo_img)
                        cv2.waitKey(1)
                        
                    await websocket.send_json(result)

    except WebSocketDisconnect:
        logger.info(f"Client disconnected from Passive WS: {client_host}")
    except Exception as e:
        logger.error(f"Passive WS Error: {e}")
    finally:
        decoder.close()
        if DEMO_MODE:
            cv2.destroyAllWindows()
        try:
            await websocket.close()
        except:
            pass


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
