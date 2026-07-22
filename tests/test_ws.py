import asyncio
import websockets
import json
import cv2
import numpy as np
import pytest

@pytest.mark.asyncio
@pytest.mark.skip(reason="Requires running server on localhost:8000")
async def test_ws():
    uri = "ws://localhost:8000/ws/verify"
    async with websockets.connect(uri) as websocket:
        # Create a mock video frame (green frame to simulate face maybe? or just random noise)
        # Actually, let's load a real face image if possible.
        # Do we have a face image?
        # Let's just create an image with a face-like oval to pass face detection.
        img = np.zeros((480, 640, 3), dtype=np.uint8)
        cv2.ellipse(img, (320, 240), (100, 150), 0, 0, 360, (200, 150, 100), -1)
        
        _, encoded = cv2.imencode('.jpg', img)
        byte_data = encoded.tobytes()
        
        # Send 10 frames
        for i in range(10):
            print(f"Sending frame {i}")
            await websocket.send(byte_data)
            
            # Receive result
            res = await websocket.recv()
            print("Received:", res)
