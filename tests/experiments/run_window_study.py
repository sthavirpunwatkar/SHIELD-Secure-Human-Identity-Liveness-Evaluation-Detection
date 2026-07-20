import os
import sys
import time
import cv2
import numpy as np
import onnxruntime as ort
import matplotlib.pyplot as plt
import csv
from scipy.signal import butter, filtfilt, welch

def bandpass_filter(signal, fps=30, low_hz=0.7, high_hz=4.0):
    nyq = 0.5 * fps
    low = low_hz / nyq
    high = high_hz / nyq
    b, a = butter(2, [low, high], btype='band')
    return filtfilt(b, a, signal)

def extract_signal(video_path):
    cap = cv2.VideoCapture(video_path)
    sig = []
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        h, w = frame.shape[:2]
        roi = frame[int(h*0.35):int(h*0.65), int(w*0.35):int(w*0.65)]
        sig.append(np.mean(roi[:, :, 1]))
    cap.release()
    return np.array(sig)

def compute_signal_quality(signal, fps=30):
    # variance
    variance = np.var(signal)
    
    # frequency spectrum
    f, pxx = welch(signal, fs=fps, nperseg=len(signal))
    
    # find dominant frequency in valid range (0.7 to 4.0 Hz -> 42 to 240 BPM)
    valid_idx = np.where((f >= 0.7) & (f <= 4.0))[0]
    if len(valid_idx) == 0:
        return 0, 0, 0, 0, 0
    
    valid_pxx = pxx[valid_idx]
    valid_f = f[valid_idx]
    
    max_idx = np.argmax(valid_pxx)
    dom_freq = valid_f[max_idx]
    est_hr = dom_freq * 60.0
    
    # SNR: ratio of power around dom_freq to total power in valid range
    peak_power = np.sum(valid_pxx[max(0, max_idx-1) : min(len(valid_pxx), max_idx+2)])
    total_power = np.sum(valid_pxx)
    snr = peak_power / (total_power - peak_power + 1e-6)
    
    peak_sharpness = peak_power / (np.mean(valid_pxx) + 1e-6)
    
    return variance, dom_freq, est_hr, snr, peak_sharpness

def run_experiment():
    video_path = "test.h264"
    if not os.path.exists(video_path):
        print(f"Error: {video_path} not found.")
        sys.exit(1)
        
    print("Extracting full signal...")
    full_signal = extract_signal(video_path)
    if len(full_signal) < 150:
        print(f"Video too short: {len(full_signal)} frames.")
        sys.exit(1)
        
    full_signal = bandpass_filter(full_signal)
    
    onnx_path = "models/rppg_1dcnn_v2.onnx"
    session = ort.InferenceSession(onnx_path)
    input_name = session.get_inputs()[0].name
    
    window_sizes = [150, 135, 120, 105, 90, 75, 60, 45, 30]
    
    results = []
    
    for w in window_sizes:
        print(f"--- Window Size: {w} ---")
        
        # Take the last 'w' frames from the first 150 frames to simulate getting w frames
        sig_window = full_signal[150 - w : 150].copy()
        
        # Signal Quality
        variance, dom_freq, est_hr, snr, peak_sharpness = compute_signal_quality(sig_window)
        
        # Normalize
        sig_window = (sig_window - np.mean(sig_window)) / (np.std(sig_window) + 1e-6)
        
        # Pad to 150 (Zero padding at the start)
        if w < 150:
            pad_width = 150 - w
            # Use zero padding (since signal is z-score normalized, 0 is the mean)
            sig_padded = np.pad(sig_window, (pad_width, 0), 'constant', constant_values=0)
        else:
            sig_padded = sig_window
            
        input_tensor = sig_padded.astype(np.float32).reshape(1, 1, 150)
        
        # Stability / Latency (20 iterations)
        latencies = []
        confidences = []
        
        for _ in range(20):
            t0 = time.time()
            out = session.run(None, {input_name: input_tensor})
            t1 = time.time()
            latencies.append((t1 - t0) * 1000.0) # ms
            confidences.append(float(out[0][0][0]))
            
        mean_conf = np.mean(confidences)
        std_conf = np.std(confidences)
        mean_lat = np.mean(latencies)
        
        results.append({
            "window_size": w,
            "variance": variance,
            "dom_freq": dom_freq,
            "est_hr": est_hr,
            "snr": snr,
            "peak_sharpness": peak_sharpness,
            "mean_confidence": mean_conf,
            "std_confidence": std_conf,
            "mean_latency_ms": mean_lat
        })
        
    # Write CSV
    with open("window_sensitivity.csv", "w", newline='') as f:
        writer = csv.DictWriter(f, fieldnames=results[0].keys())
        writer.writeheader()
        writer.writerows(results)
        
    # Plot
    sizes = [r["window_size"] for r in results]
    confs = [r["mean_confidence"] for r in results]
    stds = [r["std_confidence"] for r in results]
    snrs = [r["snr"] for r in results]
    
    fig, ax1 = plt.subplots()
    
    ax1.set_xlabel('Window Size (frames)')
    ax1.set_ylabel('Mean Confidence', color='tab:blue')
    ax1.errorbar(sizes, confs, yerr=stds, fmt='-o', color='tab:blue', label='Confidence')
    ax1.tick_params(axis='y', labelcolor='tab:blue')
    ax1.set_ylim([0, 1.1])
    ax1.invert_xaxis()
    
    ax2 = ax1.twinx()
    ax2.set_ylabel('SNR', color='tab:red')
    ax2.plot(sizes, snrs, '--s', color='tab:red', label='SNR')
    ax2.tick_params(axis='y', labelcolor='tab:red')
    
    fig.tight_layout()
    plt.title("rPPG Window Sensitivity")
    plt.savefig("window_sensitivity_plot.png")
    plt.close()
    
    print("Done.")

if __name__ == "__main__":
    run_experiment()
