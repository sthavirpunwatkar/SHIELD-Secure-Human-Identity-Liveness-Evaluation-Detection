import cv2
import numpy as np
import time
import pytest
from backend.services.fusion_service import fusion_service

@pytest.mark.skip(reason="Missing lena.jpg")
def test_real_pipeline():
    # Load lena as a mock face (YOLO detects it)
    frame = cv2.imread('lena.jpg')
    frame = cv2.resize(frame, (640, 480))

    for i in range(160):
        # slight variation
        noise = np.random.normal(0, 1, frame.shape).astype(np.int16)
        img = np.clip(frame.astype(np.int16) + noise, 0, 255).astype(np.uint8)
        
        res = fusion_service.process_frame(img, frame_number=i, capture_timestamp=str(time.time()))
        if i % 10 == 0 or i > 145:
            print(f"Frame {i}: final_score={res['confidence']} breakdown={res['details']}")
