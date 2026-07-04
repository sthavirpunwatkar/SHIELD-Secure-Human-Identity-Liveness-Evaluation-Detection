from fastapi import FastAPI, File, UploadFile, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import cv2
import numpy as np
import io
import uuid
import json
import os
import sys

# Ensure backend and project root directories are in sys.path to allow sibling imports
backend_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(backend_dir)
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from services.fusion_service import fusion_service
from services.firebase_service import firebase_service

app = FastAPI(title="SHIELD API", version="1.0.0")

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "SHIELD"}

from inference.session_manager import SessionManager

# Global Session Manager
session_manager = SessionManager()

@app.websocket("/ws/challenge")
async def websocket_challenge(websocket: WebSocket):
    """
    WebSocket endpoint for active challenge-response liveness streaming.
    Receives text messages (commands) and binary image data.
    """
    await websocket.accept()
    client_host = websocket.client.host if websocket.client else "unknown"
    print(f"Client connected to Challenge WebSocket: {client_host}")
    
    try:
        session = session_manager.create_session(client_id=client_host)
        challenge_session = session.challenge_session
    except RuntimeError as e:
        await websocket.send_json({"type": "error", "message": str(e)})
        await websocket.close()
        return

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
                except json.JSONDecodeError:
                    pass
                continue

            if "bytes" in message:
                data = message["bytes"]
                # Decode frame
                nparr = np.frombuffer(data, np.uint8)
                frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
                
                if frame is None:
                    await websocket.send_json({"type": "error", "message": "Invalid image data"})
                    continue

                # Process through Fusion Service with challenge session
                result = fusion_service.process_challenge_frame(frame, challenge_session)
                raw_landmarks = result.pop("_raw_landmarks", None)
                # Add frame to session manager (validates temporal consistency and identity)
                frame_res = session.add_frame(frame, landmarks=raw_landmarks)
                if not frame_res["accepted"]:
                    if frame_res.get("expired"):
                        await websocket.send_json({"type": "error", "message": "Session expired"})
                        break
                    if frame_res.get("reason") == "identity_swap_detected":
                        await websocket.send_json({"type": "error", "message": "Identity mismatch detected"})
                        break
                    continue
                
                # Check challenge updates
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
                        break # End session
                else:
                    # Normal frame update (can send partial progress if needed)
                    # For now, just send the frame result silently or omitted to save bandwidth
                    # We can send a generic verdict update
                    pass

    except WebSocketDisconnect:
        print(f"Client disconnected from Challenge WS: {client_host}")
    except Exception as e:
        print(f"Challenge WS Error: {e}")
    finally:
        # Cleanup the session to prevent memory leak and session limit issues
        if "session" in locals() and session.session_id in session_manager._sessions:
            try:
                del session_manager._sessions[session.session_id]
            except Exception as cleanup_err:
                print(f"Error cleaning up challenge session: {cleanup_err}")
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
    client_host = websocket.client.host if websocket.client else "unknown"
    print(f"Client connected to Passive Verify WebSocket: {client_host}")

    try:
        while True:
            message = await websocket.receive()

            if "bytes" in message:
                data = message["bytes"]
                nparr = np.frombuffer(data, np.uint8)
                frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
                if frame is None:
                    await websocket.send_json({"error": "Invalid image data"})
                    continue
                result = fusion_service.process_frame(frame)
                await websocket.send_json(result)

            elif "text" in message:
                # Ignore text messages in passive mode
                pass

    except WebSocketDisconnect:
        print(f"Client disconnected from Passive WS: {client_host}")
    except Exception as e:
        print(f"Passive WS Error: {e}")
    finally:
        try:
            await websocket.close()
        except:
            pass


@app.post("/verify")
async def verify_liveness(file: UploadFile = File(...)):
    """
    Receives an image frame and runs the SHIELD liveness detection pipeline.
    """
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Invalid file type. Please upload an image.")

    try:
        # 1. Read image from upload
        contents = await file.read()
        nparr = np.frombuffer(contents, np.uint8)
        frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        if frame is None:
            raise HTTPException(status_code=400, detail="Could not decode image.")

        # 2. Process frame through Fusion Service
        result = fusion_service.process_frame(frame)

        # 3. Log to Firebase (Async/Fire-and-forget style)
        session_id = str(uuid.uuid4())
        log_data = {
            "session_id": session_id,
            "verdict": result["verdict"],
            "confidence": result["confidence"],
            "details": result["details"]
        }
        
        # Upload snapshot if live or spoof (optional threshold)
        if result["status"] == "success":
            filename = f"{session_id}.jpg"
            # Re-encode to JPEG for storage
            _, buffer = cv2.imencode(".jpg", frame)
            image_url = firebase_service.upload_snapshot(buffer.tobytes(), filename)
            log_data["image_url"] = image_url

        # Persist metadata to Firestore
        firebase_service.log_verification(log_data)

        return {
            "session_id": session_id,
            "result": result
        }

    except Exception as e:
        print(f"Server Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
