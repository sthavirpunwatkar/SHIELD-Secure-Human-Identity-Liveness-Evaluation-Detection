import cv2
import time
import sys
import os
import numpy as np

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'backend'))
from inference.rppg_detector import RPPGDetector

def test_synthetic_signal(freq_bpm, fps=30.0, window_size=150):
    rppg = RPPGDetector(window_size=window_size)
    
    freq_hz = freq_bpm / 60.0
    t = np.arange(window_size) / fps
    # Generate sine wave + some baseline noise
    signal = np.sin(2 * np.pi * freq_hz * t) * 5.0 + 100.0 + np.random.normal(0, 0.5, window_size)
    
    rppg.signal_buffer = list(signal)
    
    # Run exact inference block from update()
    sig = np.array(rppg.signal_buffer, dtype=np.float32)
    sig = (sig - sig.mean()) / (sig.std() + 1e-6)

    if rppg.is_onnx:
        inp = np.expand_dims(np.expand_dims(sig, axis=0), axis=0)
        outputs = rppg.session.run([rppg.output_name], {rppg.input_name: inp})[0]
        score = float(outputs[0][0])
    else:
        import torch
        tensor = torch.from_numpy(sig).unsqueeze(0).unsqueeze(0).to(rppg.device)
        with torch.no_grad():
            score = rppg.model(tensor).item()
            
    print(f"BPM {freq_bpm:3d} -> Output Score: {score:.6f}")
    return score

if __name__ == '__main__':
    print("RPPG Synthetic Signal Test:")
    for bpm in [60, 75, 90, 120]:
        test_synthetic_signal(bpm)
    print("\nRPPG Constant Zero Test:")
    rppg = RPPGDetector(window_size=150)
    rppg.signal_buffer = [0.0]*150
    sig = np.array(rppg.signal_buffer, dtype=np.float32)
    sig = (sig - sig.mean()) / (sig.std() + 1e-6)
    if rppg.is_onnx:
        inp = np.expand_dims(np.expand_dims(sig, axis=0), axis=0)
        outputs = rppg.session.run([rppg.output_name], {rppg.input_name: inp})[0]
        score = float(outputs[0][0])
    print(f"Zero Signal Output Score: {score:.6f}")
