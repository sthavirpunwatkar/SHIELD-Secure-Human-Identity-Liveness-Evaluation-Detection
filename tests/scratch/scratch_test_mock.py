import pytest
import asyncio
from unittest.mock import patch, AsyncMock, MagicMock
import numpy as np

async def test_mock():
    from backend.main import websocket_challenge
    from fastapi import WebSocket
    
    mock_ws = AsyncMock(spec=WebSocket)
    mock_ws.client = MagicMock()
    mock_ws.client.host = "test_identity_mismatch_host"
    mock_ws.headers = {"x-bypass-seb": "1"}

    receive_call_count = 0
    async def mock_receive():
        nonlocal receive_call_count
        receive_call_count += 1
        if receive_call_count == 1:
            return {"text": '{"type": "start_challenge"}'}
        elif receive_call_count == 2:
            return {"text": '{"frameNumber": 1}'}
        elif receive_call_count == 3:
            return {"bytes": b"fake_frame_data_1"}
        elif receive_call_count == 4:
            from fastapi import WebSocketDisconnect
            raise WebSocketDisconnect()

    mock_ws.receive = mock_receive
    mock_ws.accept = AsyncMock()
    mock_ws.send_json = AsyncMock()
    mock_ws.close = AsyncMock()

    from backend.services.video_decoder import DecodedFrame
    with patch('backend.services.video_decoder.StreamingDecoder.decode_chunk') as mock_decode, \
         patch('backend.services.fusion_service.FusionService.process_challenge_frame') as mock_process:
        
        frame1 = DecodedFrame(image=np.zeros((480, 640, 3), dtype=np.uint8), capture_timestamp="", arrival_timestamp=1.0, frame_number=1, sequence_number=1, resolution="", metadata={})
        mock_decode.return_value = [frame1]
        
        mock_process.return_value = {"status": "success", "_raw_landmarks": None, "verdict": "Live", "confidence": 0.9, "breakdown": {}}
        
        try:
            await websocket_challenge(mock_ws)
        except Exception:
            pass
            
        print("MOCK CALLED?", mock_process.called)

asyncio.run(test_mock())
