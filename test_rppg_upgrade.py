import numpy as np
import cv2
from inference.rppg_detector import RPPGDetector
from inference.rppg_dl import DeepRPPGDetector

def test_rppg_comparison():
    print("--- SHIELD rPPG Upgrade Comparison ---")
    
    legacy_detector = RPPGDetector()
    deep_detector = DeepRPPGDetector()
    
    # Create a dummy sequence of 30 frames
    frames = []
    for i in range(30):
        # Base frame
        frame = np.ones((480, 640, 3), dtype=np.uint8) * 128
        # Simulate a face area
        cv2.rectangle(frame, (200, 100), (400, 300), (200, 200, 200), -1)
        # Add subtle green channel variation to simulate pulse
        pulse_val = 5 * np.sin(2 * np.pi * 1.0 * (i / 30.0)) # 1Hz pulse
        frame[100:300, 200:400, 1] = np.clip(frame[100:300, 200:400, 1] + pulse_val, 0, 255)
        frames.append(frame)

    print("\n1. Testing Legacy rPPG Pipeline...")
    legacy_score = 0.5
    for f in frames:
        legacy_score = legacy_detector.update(f)
    print(f"Legacy Liveness Score: {legacy_score:.4f}")

    print("\n2. Testing Deep rPPG Pipeline...")
    deep_score = deep_detector.process_sequence(frames)
    print(f"Deep rPPG Liveness Score: {deep_score:.4f}")

    print("\n--- rPPG Comparison Complete ---")

if __name__ == "__main__":
    test_rppg_comparison()
