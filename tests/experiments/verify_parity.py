import cv2
import time
import sys
import os
import numpy as np

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'backend'))
from inference.rppg_detector import RPPGDetector
from inference.yolo_detector import YoloSegDetector

def print_signal_stages(raw_signal, rppg_detector, name="Signal"):
    print(f"--- {name} ---")
    sig = np.array(raw_signal, dtype=np.float32)
    print(f"1. Raw signal (mean: {sig.mean():.2f}, std: {sig.std():.2f}): {sig[:5]}...")
    
    # 2. Filtered
    from scipy.signal import butter, filtfilt
    fps = 30.0
    nyq = 0.5 * fps
    low = 0.7 / nyq
    high = 4.0 / nyq
    b, a = butter(2, [low, high], btype='band')
    sig_filtered = filtfilt(b, a, sig)
    print(f"2. Filtered signal (mean: {sig_filtered.mean():.2f}, std: {sig_filtered.std():.2f}): {sig_filtered[:5]}...")
    
    # 3. Normalized
    sig_norm = ((sig_filtered - sig_filtered.mean()) / (sig_filtered.std() + 1e-6)).astype(np.float32)
    print(f"3. Normalized signal (mean: {sig_norm.mean():.2f}, std: {sig_norm.std():.2f}): {sig_norm[:5]}...")
    
    # 4. Model probability
    if rppg_detector.is_onnx:
        inp = np.expand_dims(np.expand_dims(sig_norm, axis=0), axis=0)
        outputs = rppg_detector.session.run([rppg_detector.output_name], {rppg_detector.input_name: inp})[0]
        score = float(outputs[0][0])
    print(f"4. Model probability: {score:.6f}\n")

if __name__ == '__main__':
    rppg = RPPGDetector(window_size=150)
    
    # Synthetic
    t = np.arange(150) / 30.0
    synth_sig = np.sin(2 * np.pi * (75/60.0) * t) * 5.0 + 100.0 + np.random.normal(0, 0.2, 150)
    print_signal_stages(synth_sig, rppg, "Synthetic 75 BPM Pulse")
    
    # Real video
    cap = cv2.VideoCapture('/home/sp/2026-07-06 20-36-14.mp4')
    yolo = YoloSegDetector()
    real_sig = []
    
    while cap.isOpened() and len(real_sig) < 150:
        ret, frame = cap.read()
        if not ret: break
        faces = yolo.detect_faces(frame)
        if faces:
            bbox = faces[0]['bbox']
            real_sig.append(rppg.extract_roi_signal(frame, bbox=bbox))
        else:
            real_sig.append(100.0)
    cap.release()
    
    print_signal_stages(real_sig, rppg, "Real Video (150 frames)")
