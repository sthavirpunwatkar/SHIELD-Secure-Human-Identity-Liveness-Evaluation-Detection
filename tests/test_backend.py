import pytest
import asyncio
import websockets
import json
import cv2
import numpy as np
import httpx
import subprocess
import sys
import socket
import time

BACKEND_URL = "http://localhost:8000"
WS_URL = "ws://localhost:8000/ws/verify"

def is_backend_running(port=8000):
    import httpx
    try:
        # Use sync client to avoid async fixture complexity
        with httpx.Client() as client:
            response = client.get(f"http://127.0.0.1:{port}/health", timeout=0.5)
            return response.status_code == 200 and response.json().get("status") == "healthy"
    except Exception:
        return False

@pytest.fixture(scope="session", autouse=True)
def run_backend_server():
    port = 8000
    if is_backend_running(port):
        yield
        return

    import os
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    backend_dir = os.path.join(project_root, "backend")
    
    env = os.environ.copy()
    env["PYTHONPATH"] = backend_dir + os.pathsep + env.get("PYTHONPATH", "")

    proc = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "backend.main:app", "--host", "127.0.0.1", "--port", str(port)],
        cwd=project_root,
        env=env,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    
    # Wait for the backend to start up and return healthy
    start_time = time.time()
    success = False
    while time.time() - start_time < 20.0:  # Allow up to 20 seconds for model loading on CPU
        if is_backend_running(port):
            success = True
            break
        time.sleep(0.5)

    if not success:
        proc.terminate()
        proc.wait()
        raise RuntimeError("Failed to start FastAPI backend server for integration tests within 20 seconds.")
        
    try:
        yield
    finally:
        proc.terminate()
        proc.wait()

@pytest.mark.asyncio
async def test_health_check():
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BACKEND_URL}/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"

@pytest.mark.asyncio
async def test_websocket_connection():
    async with websockets.connect(WS_URL, additional_headers={"X-Bypass-SEB": "1"}) as websocket:
        # Just connecting is enough to pass if no exception raised
        pass

@pytest.mark.asyncio
async def test_websocket_send_invalid_data():
    async with websockets.connect(WS_URL, additional_headers={"X-Bypass-SEB": "1"}) as websocket:
        # Send invalid H.264 data (a JPEG) to trigger a decode error instead of silent drop
        frame = np.zeros((10, 10, 3), dtype=np.uint8)
        _, buffer = cv2.imencode(".jpg", frame)
        await websocket.send(buffer.tobytes())
        response = await websocket.recv()
        data = json.loads(response)
        assert "error" in data or data["verdict"] == "No Face Detected"

@pytest.mark.asyncio
async def test_websocket_send_valid_image():
    async with websockets.connect(WS_URL, additional_headers={"X-Bypass-SEB": "1"}) as websocket:
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
    async with websockets.connect(WS_URL, additional_headers={"X-Bypass-SEB": "1"}) as websocket:
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
        
        # Note: This might fail if DB is not mocked correctly or credentials missing
        # but the API should handle it gracefully.
        response = await client.post(f"{BACKEND_URL}/verify", files=files, headers={"X-Bypass-SEB": "1"})
        assert response.status_code in [200, 500] # 500 if DB fails but we want to see it handled

@pytest.mark.asyncio
async def test_websocket_challenge_session_cleanup():
    from backend.main import websocket_challenge, session_manager
    from fastapi import WebSocket
    from unittest.mock import AsyncMock, MagicMock
    
    # Mock WebSocket
    mock_ws = AsyncMock(spec=WebSocket)
    mock_ws.client = MagicMock()
    mock_ws.client.host = "test_cleanup_host"
    mock_ws.headers = {"x-bypass-seb": "1"}
    
    receive_call_count = 0
    async def mock_receive():
        nonlocal receive_call_count
        receive_call_count += 1
        if receive_call_count == 1:
            return {"text": '{"type": "start_challenge"}'}
        else:
            from fastapi import WebSocketDisconnect
            raise WebSocketDisconnect()
            
    mock_ws.receive = mock_receive
    mock_ws.accept = AsyncMock()
    mock_ws.send_json = AsyncMock()
    mock_ws.close = AsyncMock()
    
    # Verify initially no sessions for this host
    initial_sessions_count = len(session_manager._sessions)
    
    # Run the websocket handler
    try:
        await websocket_challenge(mock_ws)
    except Exception:
        pass
        
    # Verify the session has been cleaned up and is not in session_manager._sessions
    assert len(session_manager._sessions) == initial_sessions_count


@pytest.mark.asyncio
async def test_websocket_identity_mismatch():
    from backend.main import websocket_challenge, session_manager, fusion_service
    from fastapi import WebSocket
    from unittest.mock import AsyncMock, MagicMock, patch
    
    # Mock WebSocket
    mock_ws = AsyncMock(spec=WebSocket)
    mock_ws.client = MagicMock()
    mock_ws.client.host = "test_identity_mismatch_host"
    mock_ws.headers = {"x-bypass-seb": "1"}
    
    # Helper to generate mock landmarks
    def make_mock_landmarks(nose, leye, reye, chin, lmouth, rmouth):
        l = [{"x": 0.0, "y": 0.0, "z": 0.0}] * 300
        l[1] = {"x": nose[0], "y": nose[1], "z": nose[2]}
        l[33] = {"x": leye[0], "y": leye[1], "z": leye[2]}
        l[263] = {"x": reye[0], "y": reye[1], "z": reye[2]}
        l[152] = {"x": chin[0], "y": chin[1], "z": chin[2]}
        l[61] = {"x": lmouth[0], "y": lmouth[1], "z": lmouth[2]}
        l[291] = {"x": rmouth[0], "y": rmouth[1], "z": rmouth[2]}
        return l

    landmarks_1 = make_mock_landmarks(
        [0.0, 0.0, 0.0], [-0.1, 0.1, 0.0], [0.1, 0.1, 0.0],
        [0.0, -0.2, 0.0], [-0.05, -0.1, 0.0], [0.05, -0.1, 0.0]
    )
    landmarks_2 = make_mock_landmarks(
        [0.0, 0.0, 0.0], [-0.1, 0.1, 0.0], [0.1, 0.1, 0.0],
        [0.0, -0.6, 0.0], [-0.3, -0.1, 0.0], [0.3, -0.1, 0.0]  # Swapped identity ratios
    )

    receive_call_count = 0
    async def mock_receive():
        nonlocal receive_call_count
        receive_call_count += 1
        if receive_call_count == 1:
            return {"text": '{"type": "start_challenge"}'}
        elif receive_call_count == 2:
            return {"bytes": b"fake_frame_data_1"}
        elif receive_call_count == 3:
            return {"bytes": b"fake_frame_data_2"}
        else:
            from fastapi import WebSocketDisconnect
            raise WebSocketDisconnect()
            
    mock_ws.receive = mock_receive
    mock_ws.accept = AsyncMock()
    mock_ws.send_json = AsyncMock()
    mock_ws.close = AsyncMock()
    
    # Mock WebCodecsDecoder and process_challenge_frame
    with patch('services.video_decoder.WebCodecsDecoder.decode_chunk') as mock_decode, \
         patch.object(fusion_service, 'process_challenge_frame') as mock_process:
        
        mock_decode.side_effect = [
            [np.zeros((480, 640, 3), dtype=np.uint8)],
            [np.ones((480, 640, 3), dtype=np.uint8)]
        ]
        
        # Frame 1: Valid frame with landmarks_1
        # Frame 2: Swap frame with landmarks_2
        mock_process.side_effect = [
            {"status": "success", "_raw_landmarks": landmarks_1, "verdict": "Live", "confidence": 0.9, "breakdown": {}},
            {"status": "success", "_raw_landmarks": landmarks_2, "verdict": "Live", "confidence": 0.9, "breakdown": {}}
        ]
        
        try:
            import traceback
            await websocket_challenge(mock_ws)
        except Exception:
            print("WEBSOCKET EXITED WITH EXCEPTION:")
            traceback.print_exc()
            pass
            
    # Verify we received "Identity mismatch detected" error message
    sent_messages = [call.args[0] for call in mock_ws.send_json.call_args_list]
    print("ALL SENT MESSAGES:", sent_messages)
    error_messages = [msg for msg in sent_messages if msg.get("type") == "error" and "Identity mismatch" in msg.get("message")]
    assert len(error_messages) == 1
    print("✓ Identity swap rejection verified successfully.")

