from fastapi import FastAPI, File, UploadFile, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import cv2
import numpy as np
import io
import uuid
import json
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

@app.websocket("/ws/verify")
async def websocket_verify(websocket: WebSocket):
    """
    WebSocket endpoint for real-time liveness streaming.
    Receives binary image data and returns JSON analysis.
    """
    await websocket.accept()
    print(f"Client connected to WebSocket: {websocket.client}")
    
    try:
        while True:
            # Receive binary frame data
            data = await websocket.receive_bytes()
            
            # Decode frame
            nparr = np.frombuffer(data, np.uint8)
            frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            
            if frame is None:
                await websocket.send_json({"error": "Could not decode frame"})
                continue

            # Process through Fusion Service
            result = fusion_service.process_frame(frame)
            
            # Send result back instantly
            await websocket.send_json(result)
            
            # Optional: Log to Firebase in the background if verdict is conclusive
            if result["verdict"] in ["Live", "Spoof"]:
                # (You could use a background task here for even better performance)
                pass

    except WebSocketDisconnect:
        print(f"Client disconnected: {websocket.client}")
    except Exception as e:
        print(f"WebSocket Error: {e}")
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
