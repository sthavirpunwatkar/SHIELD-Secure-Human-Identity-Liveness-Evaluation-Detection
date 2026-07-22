import sys
import os
import time
import numpy as np
import torch

sys.path.append(os.path.abspath(os.path.dirname(__file__)))
from inference.rppg_detector import RPPGDetector
from training.train_rppg_v2 import generate_live_signal

def create_frame(green_val, blank=False):
    if blank:
        return np.zeros((480, 640, 3), dtype=np.uint8)
    
    # Base skin tone
    frame = np.full((480, 640, 3), [100, 150, 200], dtype=np.float32) # BGR
    # Add green variation
    frame[:, :, 1] += green_val * 10.0 # scale up signal for visibility in RGB
    return np.clip(frame, 0, 255).astype(np.uint8)

def run_scenario(name, signal, blank=False):
    print(f"\n{'='*80}")
    print(f"SCENARIO: {name}")
    print(f"{'='*80}")
    
    detector = RPPGDetector(window_size=150)
    
    # Mock bbox to hit the runtime branch
    bbox = [200, 100, 440, 340]
    
    for i in range(150):
        val = signal[i] if signal is not None else 0.0
        frame = create_frame(val, blank=blank)
        
        from backend.services.fusion_service import fusion_service
        # Only print the last frame's output to keep logs clean
        # We temporarily hijack sys.stdout
        if i < 149:
            import contextlib, io
            with contextlib.redirect_stdout(io.StringIO()):
                fusion_service.process_frame(frame, frame_number=i, capture_timestamp=str(time.time()))
        else:
            fusion_service.process_frame(frame, frame_number=i, capture_timestamp=str(time.time()))
            
if __name__ == "__main__":
    # 1. Real human (live signal)
    live_sig = generate_live_signal(150, fps=30)
    run_scenario("Real human (30 seconds)", live_sig)
    
    # 2. Printed photograph (flat signal, noise only)
    photo_sig = np.random.randn(150).astype(np.float32) * 0.01 
    run_scenario("Printed photograph (30 seconds)", photo_sig)
    
    # 3. Blank camera
    run_scenario("Blank camera (30 seconds)", None, blank=True)
