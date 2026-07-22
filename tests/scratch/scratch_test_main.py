import pytest
import asyncio
from unittest.mock import patch, AsyncMock, MagicMock
import numpy as np
import sys
import os
sys.path.insert(0, os.path.abspath('backend'))

async def test_main():
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
            return {"text": '{"frameNumber": 2}'}
        elif receive_call_count == 5:
            return {"bytes": b"fake_frame_data_2"}
        else:
            from fastapi import WebSocketDisconnect
            raise WebSocketDisconnect()

    mock_ws.receive = mock_receive
    mock_ws.accept = AsyncMock()
    mock_ws.send_json = AsyncMock()
    mock_ws.close = AsyncMock()

    def make_mock_landmarks(nose, leye, reye, chin, lmouth, rmouth):
        l = [{"x": 0.0, "y": 0.0, "z": 0.0}] * 300
        l[1] = {"x": nose[0], "y": nose[1], "z": nose[2]}
        l[33] = {"x": leye[0], "y": leye[1], "z": leye[2]}
        l[263] = {"x": reye[0], "y": reye[1], "z": reye[2]}
        l[152] = {"x": chin[0], "y": chin[1], "z": chin[2]}
        l[61] = {"x": lmouth[0], "y": lmouth[1], "z": lmouth[2]}
        l[291] = {"x": rmouth[0], "y": rmouth[1], "z": rmouth[2]}
        return l

    landmarks_1 = make_mock_landmarks([0.0, 0.0, 0.0], [-0.1, 0.1, 0.0], [0.1, 0.1, 0.0], [0.0, -0.2, 0.0], [-0.05, -0.1, 0.0], [0.05, -0.1, 0.0])
    landmarks_2 = make_mock_landmarks([0.0, 0.0, 0.0], [-0.1, 0.1, 0.0], [0.1, 0.1, 0.0], [0.0, -0.6, 0.0], [-0.3, -0.1, 0.0], [0.3, -0.1, 0.0])

    from backend.services.video_decoder import StreamingDecoder, DecodedFrame
    from backend.services.fusion_service import FusionService
    with patch.object(StreamingDecoder, 'decode_chunk') as mock_decode, \
         patch.object(FusionService, 'process_challenge_frame') as mock_process:
        
        frame1 = DecodedFrame(image=np.zeros((480, 640, 3), dtype=np.uint8), capture_timestamp="", arrival_timestamp=1.0, frame_number=1, sequence_number=1, resolution="", metadata={})
        frame2 = DecodedFrame(image=np.ones((480, 640, 3), dtype=np.uint8), capture_timestamp="", arrival_timestamp=1.0, frame_number=2, sequence_number=2, resolution="", metadata={})
        
        mock_decode.side_effect = [[frame1], [frame2]]
        
        mock_process.side_effect = [
            {"status": "success", "_raw_landmarks": landmarks_1, "verdict": "Live", "confidence": 0.9, "breakdown": {}},
            {"status": "success", "_raw_landmarks": landmarks_2, "verdict": "Live", "confidence": 0.9, "breakdown": {}}
        ]
        
        await websocket_challenge(mock_ws)
        
        sent_messages = [call.args[0] for call in mock_ws.send_json.call_args_list]
        print("ALL SENT MESSAGES:", sent_messages)

asyncio.run(test_main())
