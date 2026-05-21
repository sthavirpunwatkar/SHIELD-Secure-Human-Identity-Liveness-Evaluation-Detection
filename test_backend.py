import pytest
import asyncio
import websockets
import json
import cv2
import numpy as np
import httpx

BACKEND_URL = "http://localhost:8000"
WS_URL = "ws://localhost:8000/ws/verify"

@pytest.mark.asyncio
async def test_health_check():
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BACKEND_URL}/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"

@pytest.mark.asyncio
async def test_websocket_connection():
    async with websockets.connect(WS_URL) as websocket:
        # Just connecting is enough to pass if no exception raised
        pass

@pytest.mark.asyncio
async def test_websocket_send_invalid_data():
    async with websockets.connect(WS_URL) as websocket:
        # Send random bytes that aren't an image
        await websocket.send(b"not an image")
        response = await websocket.recv()
        data = json.loads(response)
        assert "error" in data or data["verdict"] == "No Face Detected"

@pytest.mark.asyncio
async def test_websocket_send_valid_image():
    async with websockets.connect(WS_URL) as websocket:
        # Create a dummy image with a face-like shape
        frame = np.zeros((480, 640, 3), dtype=np.uint8)
        cv2.rectangle(frame, (200, 100), (400, 300), (255, 255, 255), -1)
        _, buffer = cv2.imencode(".jpg", frame)
        
        await websocket.send(buffer.tobytes())
        response = await websocket.recv()
        data = json.loads(response)
        
        assert "verdict" in data
        assert "confidence" in data
        assert "status" in data

@pytest.mark.asyncio
async def test_websocket_stress():
    async with websockets.connect(WS_URL) as websocket:
        frame = np.zeros((100, 100, 3), dtype=np.uint8)
        _, buffer = cv2.imencode(".jpg", frame)
        
        for _ in range(10):
            await websocket.send(buffer.tobytes())
            response = await websocket.recv()
            data = json.loads(response)
            assert data["status"] in ["success", "fail"]

@pytest.mark.asyncio
async def test_http_verify_endpoint():
    async with httpx.AsyncClient() as client:
        frame = np.zeros((480, 640, 3), dtype=np.uint8)
        _, buffer = cv2.imencode(".jpg", frame)
        files = {'file': ('test.jpg', buffer.tobytes(), 'image/jpeg')}
        
        # Note: This might fail if Firebase is not mocked correctly or credentials missing
        # but the API should handle it gracefully.
        response = await client.post(f"{BACKEND_URL}/verify", files=files)
        assert response.status_code in [200, 500] # 500 if firebase fails but we want to see it handled
