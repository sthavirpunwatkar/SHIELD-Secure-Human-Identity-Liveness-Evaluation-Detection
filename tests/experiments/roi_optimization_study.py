import cv2
import time
import sys
import os
import numpy as np
from scipy.signal import butter, filtfilt, welch

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'backend'))
from inference.behavioral_analyzer import BehavioralAnalyzer
from inference.yolo_detector import YoloSegDetector
from inference.rppg_detector import RPPGDetector

def get_roi_signals(frame, bbox, landmarks, w, h):
    signals = {}
    x1, y1, x2, y2 = [int(v) for v in bbox]
    x1, y1 = max(0, x1), max(0, y1)
    x2, y2 = min(w, x2), min(h, y2)
    box_w, box_h = x2 - x1, y2 - y1
    
    if box_w <= 0 or box_h <= 0:
        return None
        
    # 1. Entire face
    roi_entire = frame[y1:y2, x1:x2]
    signals['entire_face'] = np.mean(roi_entire[:, :, 1]) if roi_entire.size > 0 else 0
    
    # 2. Forehead (top 15% to 35%, middle 50%)
    fy1, fy2 = y1 + int(box_h * 0.15), y1 + int(box_h * 0.35)
    fx1, fx2 = x1 + int(box_w * 0.25), x1 + int(box_w * 0.75)
    roi_forehead = frame[fy1:fy2, fx1:fx2]
    forehead_val = np.mean(roi_forehead[:, :, 1]) if roi_forehead.size > 0 else 0
    signals['forehead'] = forehead_val
    
    # 3. Left cheek (Y: 50%-75%, X: 20%-40%)
    ly1, ly2 = y1 + int(box_h * 0.50), y1 + int(box_h * 0.75)
    lx1, lx2 = x1 + int(box_w * 0.20), x1 + int(box_w * 0.40)
    roi_lcheek = frame[ly1:ly2, lx1:lx2]
    lcheek_val = np.mean(roi_lcheek[:, :, 1]) if roi_lcheek.size > 0 else 0
    signals['left_cheek'] = lcheek_val
    
    # 4. Right cheek (Y: 50%-75%, X: 60%-80%)
    ry1, ry2 = y1 + int(box_h * 0.50), y1 + int(box_h * 0.75)
    rx1, rx2 = x1 + int(box_w * 0.60), x1 + int(box_w * 0.80)
    roi_rcheek = frame[ry1:ry2, rx1:rx2]
    rcheek_val = np.mean(roi_rcheek[:, :, 1]) if roi_rcheek.size > 0 else 0
    signals['right_cheek'] = rcheek_val
    
    # 5. Both cheeks
    signals['both_cheeks'] = (lcheek_val + rcheek_val) / 2
    
    # 6. Forehead + cheeks
    signals['forehead_cheeks'] = (forehead_val + lcheek_val + rcheek_val) / 3
    
    # 7. MediaPipe skin mask
    if landmarks:
        mask = np.zeros((h, w), dtype=np.uint8)
        pts = np.array([[(lm.x * w), (lm.y * h)] for lm in landmarks], dtype=np.int32)
        hull = cv2.convexHull(pts)
        cv2.fillConvexPoly(mask, hull, 1)
        skin_pixels = frame[mask == 1]
        signals['mediapipe_mask'] = np.mean(skin_pixels[:, 1]) if skin_pixels.size > 0 else 0
    else:
        signals['mediapipe_mask'] = 0
        
    return signals

def compute_metrics(sig, fps=30):
    sig = np.array(sig)
    if len(sig) == 0 or np.std(sig) == 0:
        return 0, 0, 0, 0, 0
    
    temp_var = np.var(sig)
    
    # Detrend and bandpass filter (0.7 to 3.0 Hz -> 42 to 180 bpm)
    sig_detrend = sig - np.mean(sig)
    nyq = 0.5 * fps
    b, a = butter(3, [0.7 / nyq, 3.0 / nyq], btype='band')
    sig_filt = filtfilt(b, a, sig_detrend)
    
    pulse_amp = np.std(sig_filt)
    
    # FFT
    freqs, psd = welch(sig_filt, fs=fps, nperseg=len(sig_filt))
    
    valid_idx = np.where((freqs >= 0.7) & (freqs <= 3.0))[0]
    if len(valid_idx) == 0:
        return temp_var, pulse_amp, 0, 0, 0
        
    valid_freqs = freqs[valid_idx]
    valid_psd = psd[valid_idx]
    
    peak_idx = np.argmax(valid_psd)
    hr_freq = valid_freqs[peak_idx]
    
    # SNR: ratio of power around peak to total power in band
    peak_power = np.sum(valid_psd[max(0, peak_idx-1):min(len(valid_psd), peak_idx+2)])
    total_power = np.sum(valid_psd)
    snr = 10 * np.log10(peak_power / (total_power - peak_power + 1e-6) + 1e-6)
    
    fft_quality = peak_power / total_power
    
    hr_stability = hr_freq * 60 # BPM
    
    return temp_var, pulse_amp, fft_quality, snr, hr_stability

def run_study():
    video_path = '/home/sp/2026-07-06 20-36-14.mp4'
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    if fps == 0 or np.isnan(fps):
        fps = 30.0
    
    yolo = YoloSegDetector()
    analyzer = BehavioralAnalyzer()
    rppg = RPPGDetector(window_size=150)
    
    all_signals = {
        'entire_face': [],
        'forehead': [],
        'left_cheek': [],
        'right_cheek': [],
        'both_cheeks': [],
        'forehead_cheeks': [],
        'mediapipe_mask': []
    }
    
    count = 0
    # Process 200 frames to get a good window
    while cap.isOpened() and count < 200:
        ret, frame = cap.read()
        if not ret: break
        
        h, w = frame.shape[:2]
        faces = yolo.detect_faces(frame)
        if not faces:
            continue
        bbox = faces[0]['bbox']
        
        res = analyzer.analyze(frame)
        landmarks = res.get('raw_landmarks')
        
        sigs = get_roi_signals(frame, bbox, landmarks, w, h)
        if sigs:
            for k, v in sigs.items():
                all_signals[k].append(v)
        
        count += 1
    
    cap.release()
    
    print("ROI Optimization Study Results:")
    print("-" * 115)
    print(f"{'ROI':<18} | {'Temp Var':<10} | {'Pulse Amp':<10} | {'FFT Qual':<10} | {'SNR (dB)':<10} | {'HR (BPM)':<10} | {'RPPG Conf':<10}")
    print("-" * 115)
    
    best_roi = None
    best_snr = -999
    
    for roi_name, sig in all_signals.items():
        if len(sig) < 150:
            continue
            
        temp_var, pulse_amp, fft_quality, snr, hr_stability = compute_metrics(sig, fps)
        
        sig_arr = np.array(sig[:150], dtype=np.float32)
        if len(sig_arr) == 150:
            sig_norm = (sig_arr - sig_arr.mean()) / (sig_arr.std() + 1e-6)
            
            if rppg.is_onnx:
                inp = np.expand_dims(np.expand_dims(sig_norm, axis=0), axis=0)
                outputs = rppg.session.run([rppg.output_name], {rppg.input_name: inp})[0]
                conf = float(outputs[0][0])
            else:
                import torch
                tensor = torch.from_numpy(sig_norm).unsqueeze(0).unsqueeze(0).to(rppg.device)
                with torch.no_grad():
                    conf = rppg.model(tensor).item()
        else:
            conf = 0.0
            
        print(f"{roi_name:<18} | {temp_var:<10.2f} | {pulse_amp:<10.4f} | {fft_quality:<10.4f} | {snr:<10.2f} | {hr_stability:<10.1f} | {conf:<10.4f}")
        
        if snr > best_snr:
            best_snr = snr
            best_roi = roi_name
            
    print("-" * 115)
    print(f"Recommended ROI: {best_roi} (SNR: {best_snr:.2f} dB)")

if __name__ == '__main__':
    run_study()
