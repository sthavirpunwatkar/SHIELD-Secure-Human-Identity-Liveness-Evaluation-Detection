import pytest, asyncio, websockets, json, cv2, numpy as np
WS_URL = "ws://localhost:8000/ws/verify"
async def test_it():
    async with websockets.connect(WS_URL, additional_headers={"X-Bypass-SEB": "1"}) as websocket:
        frame = np.zeros((10, 10, 3), dtype=np.uint8)
        _, buffer = cv2.imencode(".jpg", frame)
        await websocket.send(buffer.tobytes())
        response = await websocket.recv()
        data = json.loads(response)
        assert "error" in data or data.get("verdict") == "No Face Detected"
        print("PASS:", data)
asyncio.run(test_it())
