import os
import sys
import cv2
import numpy as np
import pandas as pd
import json

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from inference.rppg_detector import RPPGDetector

def run_experiment():
    detector = RPPGDetector(window_size=150)
    detector.reset()

    print("Running Experiment: Low amplitude sine wave + noise")
    
    np.random.seed(42)
    for i in range(155):
        # Base 128, amplitude 0.5, noise std 2.0 (typical for real rPPG before filtering)
        signal_val = 128.0 + 0.5 * np.sin(2 * np.pi * i / 30.0) + np.random.normal(0, 2.0)
        
        # clamp to 0-255
        intensity = max(0, min(255, int(signal_val)))
        
        frame = np.zeros((480, 640, 3), dtype=np.uint8)
        frame[:, :, 1] = intensity
        
        bbox = [100, 100, 300, 400]
        score = detector.update(frame, bbox=bbox)
        
    print(f"Final Score: {score}")

if __name__ == "__main__":
    run_experiment()
