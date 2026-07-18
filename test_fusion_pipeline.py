import sys
import os

# Ensure backend can be imported
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "backend"))
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from inference.fusion_engine import FusionEngine
from backend.services.fusion_service import fusion_service
import numpy as np

def run_tests():
    import logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s | %(levelname)s | %(message)s')
    engine = FusionEngine()

    print("--- SHIELD LIVENESS PIPELINE VALIDATION ---")

    # 1. Real Face (has pulse, blinks, high spatial score)
    # We simulate the values that the detectors would output
    res = engine.fuse(rppg_score=0.85, blink_score=1.0, antispoof_score=0.92)
    print(f"[Real Face] Final Score: {res['final_score']} -> Verdict: {res['verdict']}")
    print(f"   Breakdown: {res['breakdown']}")
    print(f"   Weights: {res['weights']}\n")

    # 2. Printed Photo (no pulse, no blinks, medium-high spatial score from static 2D image)
    # Before the fix, rppg_score was defaulting to 0.5 when initializing.
    # We test the new fixed state where rppg_score = 0.0, blink_score = 0.0
    res = engine.fuse(rppg_score=0.0, blink_score=0.0, antispoof_score=0.75)
    print(f"[Printed Photo] Final Score: {res['final_score']} -> Verdict: {res['verdict']}")
    print(f"   Breakdown: {res['breakdown']}")
    print(f"   Weights: {res['weights']}")
    print(f"   (This would previously pass with 50-56% score!)\n")

    # 3. Replay Attack (might have blinks and pulse if high quality video, but low spatial score)
    res = engine.fuse(rppg_score=0.60, blink_score=1.0, antispoof_score=0.15)
    print(f"[Replay Attack] Final Score: {res['final_score']} -> Verdict: {res['verdict']}")
    print(f"   Breakdown: {res['breakdown']}")
    print(f"   Reason: {res['reason']}\n")

    # 4. Sequential Frames Test
    print("\n--- Pipeline Tracing (Sequence) ---")
    import cv2
    # Create a mock face image that passes YOLO and Quality, but fails Anti-Spoof
    mock_img = np.zeros((480, 640, 3), dtype=np.uint8)
    # Draw a face to trick YOLO maybe?
    
    # Let's just mock the antispoof and behavioral models directly on the fusion_service instance
    from backend.services.fusion_service import fusion_service
    import time
    
    # Mock models to pass face detection but fail antispoof early exit
    class MockDetector:
        def detect_faces(self, frame):
            return [{"bbox": [100, 100, 300, 300], "is_mask_spoof": False}]
        def crop_face(self, frame, bbox):
            return frame
            
    class MockQuality:
        def evaluate(self, frame, crop):
            return {"passes_gate": True, "quality_score": 1.0, "metrics": {}}
            
    class MockBehavioral:
        def analyze(self, frame, faces=None):
            return {"landmarks_found": True, "raw_landmarks": [[0,0]], "blink_count": 0}
            
    class MockAntispoof:
        def predict(self, crop):
            return 0.10 # FAILS early exit threshold (< 0.25)
            
    # Override
    fusion_service.detector = MockDetector()
    fusion_service.quality_engine = MockQuality()
    fusion_service.behavioral = MockBehavioral()
    fusion_service.antispoof = MockAntispoof()
    
    for i in range(5):
        res = fusion_service.process_frame(mock_img, frame_number=i, capture_timestamp=str(time.time()))
        print(f"Frame {i}: rPPG Buffer Size = {len(fusion_service.rppg.signal_buffer)}")
        
if __name__ == "__main__":
    run_tests()
