import os
import sys
import cv2
import numpy as np
import math
import random
import json
import matplotlib.pyplot as plt
from scipy.signal import butter, filtfilt, welch
import scipy.stats as stats
import torch
import onnxruntime as ort

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from training.models.rppg_cnn import get_model as get_rppg_model
from inference.yolo_detector import YoloSegDetector

# --- 1. Signal Generation & Extraction ---
def generate_raw_synthetic_signal(window_size=150, fps=30):
    n = window_size
    t = np.linspace(0, n / fps, n, dtype=np.float32)

    bpm = random.uniform(55, 100)
    cardiac_freq = bpm / 60.0
    phase = random.uniform(0, 2 * math.pi)
    cardiac = np.sin(2 * math.pi * cardiac_freq * t + phase)

    resp_bpm = random.uniform(12, 25)
    resp_freq = resp_bpm / 60.0
    resp = 1.0 + 0.15 * np.sin(2 * math.pi * resp_freq * t)
    cardiac = cardiac * resp

    harmonic = 0.3 * np.sin(2 * 2 * math.pi * cardiac_freq * t + phase + 0.5)

    motion = np.cumsum(np.random.randn(n).astype(np.float32)) * 0.02
    motion = motion - motion.mean()

    noise = np.random.randn(n).astype(np.float32) * 0.05
    # Do NOT normalize here so we have the raw signal
    return cardiac + harmonic + motion + noise

def get_raw_real_signal(video_path='/home/sp/2026-07-06 20-36-14.mp4', window_size=150):
    cap = cv2.VideoCapture(video_path)
    yolo = YoloSegDetector()
    buffer = []
    
    while cap.isOpened() and len(buffer) < window_size:
        ret, frame = cap.read()
        if not ret: break
        faces = yolo.detect_faces(frame)
        if not faces: continue
        
        x1, y1, x2, y2 = [int(v) for v in faces[0]['bbox']]
        h, w = frame.shape[:2]
        x1, y1 = max(0, x1), max(0, y1)
        x2, y2 = min(w, x2), min(h, y2)
        box_w, box_h = x2 - x1, y2 - y1
        
        if box_h > 0 and box_w > 0:
            roi_y1 = y1 + int(box_h * 0.50)
            roi_y2 = y1 + int(box_h * 0.75)
            roi_x1 = x1 + int(box_w * 0.60)
            roi_x2 = x1 + int(box_w * 0.80)
            roi = frame[roi_y1:roi_y2, roi_x1:roi_x2]
            if roi.size > 0:
                buffer.append(float(np.mean(roi[:, :, 1])))
    
    cap.release()
    return np.array(buffer, dtype=np.float32)

# --- 2. Processing Steps ---
def apply_bandpass(sig, fps=30.0):
    nyq = 0.5 * fps
    b, a = butter(2, [0.7 / nyq, 4.0 / nyq], btype='band')
    return filtfilt(b, a, sig)

def apply_zscore(sig):
    return (sig - sig.mean()) / (sig.std() + 1e-6)

# --- 3. Compute Metrics ---
def compute_metrics(sig, fps=30.0):
    sig = np.array(sig, dtype=np.float32)
    mean = np.mean(sig)
    std = np.std(sig)
    minimum = np.min(sig)
    maximum = np.max(sig)
    
    # Detrend for FFT to get clean frequency components
    sig_detrend = sig - mean
    energy = np.sum(sig_detrend ** 2)
    amplitude = (maximum - minimum) / 2.0
    
    freqs, psd = welch(sig_detrend, fs=fps, nperseg=len(sig))
    valid_idx = np.where((freqs >= 0.7) & (freqs <= 4.0))[0]
    
    if len(valid_idx) > 0:
        valid_freqs = freqs[valid_idx]
        valid_psd = psd[valid_idx]
        peak_idx = np.argmax(valid_psd)
        fft_peak = valid_freqs[peak_idx]
        peak_power = np.sum(valid_psd[max(0, peak_idx-1):min(len(valid_psd), peak_idx+2)])
        total_power = np.sum(valid_psd)
        snr = 10 * np.log10(peak_power / (total_power - peak_power + 1e-6) + 1e-6)
    else:
        fft_peak = 0
        snr = 0
        
    return {
        "mean": float(mean),
        "std": float(std),
        "min": float(minimum),
        "max": float(maximum),
        "fft_peak": float(fft_peak),
        "amplitude": float(amplitude),
        "energy": float(energy),
        "snr": float(snr),
        "length": int(len(sig)),
        "dtype": str(sig.dtype),
        "shape": list(sig.shape)
    }

# --- 4. Activation Inspection & Model Run ---
activations = {}
def get_activation(name):
    def hook(model, input, output):
        activations[name] = output.detach().cpu().numpy()
    return hook

def run_experiment():
    out_dir = "docs/experiments/pr0055"
    os.makedirs(out_dir, exist_ok=True)
    
    raw_synth = generate_raw_synthetic_signal()
    raw_real = get_raw_real_signal()
    
    # Build cases
    cases = {
        "A_Synth_NoBandpass": apply_zscore(raw_synth),
        "B_Synth_Bandpass": apply_zscore(apply_bandpass(raw_synth)),
        "C_Real_NoBandpass": apply_zscore(raw_real),
        "D_Real_Bandpass": apply_zscore(apply_bandpass(raw_real))
    }
    
    # Load Model
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model = get_rppg_model(window_size=150)
    model.load_state_dict(torch.load("models/rppg_1dcnn_v2.pt", map_location=device, weights_only=True))
    model.to(device)
    model.eval()
    
    # Register hooks on Conv1d layers
    hook_handles = []
    for name, layer in model.named_modules():
        if isinstance(layer, torch.nn.Conv1d):
            hook_handles.append(layer.register_forward_hook(get_activation(name)))
    
    results = {}
    activation_stats = {}
    
    for case_name, processed_sig in cases.items():
        metrics = compute_metrics(processed_sig)
        
        # Inference
        processed_sig = processed_sig.astype(np.float32)
        tensor = torch.from_numpy(processed_sig).unsqueeze(0).unsqueeze(0).to(device)
        with torch.no_grad():
            prob = model(tensor).item()
            
        metrics["probability"] = prob
        results[case_name] = metrics
        
        # Record activations
        activation_stats[case_name] = {}
        for layer_name, act in activations.items():
            activation_stats[case_name][layer_name] = {
                "mean": float(np.mean(act)),
                "std": float(np.std(act)),
                "max": float(np.max(act))
            }
            
    # Cleanup hooks
    for h in hook_handles:
        h.remove()
        
    # Plotting
    for name, sig in cases.items():
        plt.figure(figsize=(10, 4))
        plt.plot(sig)
        plt.title(f"Normalized Signal - {name}")
        plt.xlabel("Frames")
        plt.ylabel("Z-score")
        plt.tight_layout()
        plt.savefig(os.path.join(out_dir, f"{name}_signal.png"))
        plt.close()
        
        # FFT Plot
        freqs, psd = welch(sig, fs=30.0, nperseg=len(sig))
        plt.figure(figsize=(10, 4))
        plt.plot(freqs, psd)
        plt.title(f"Power Spectrum - {name}")
        plt.xlabel("Frequency (Hz)")
        plt.ylabel("Power")
        plt.xlim(0, 5)
        plt.tight_layout()
        plt.savefig(os.path.join(out_dir, f"{name}_fft.png"))
        plt.close()

    # KL Divergence (approximation using histograms)
    def compute_kl(sig1, sig2):
        min_val = min(np.min(sig1), np.min(sig2))
        max_val = max(np.max(sig1), np.max(sig2))
        bins = np.linspace(min_val, max_val, 30)
        p, _ = np.histogram(sig1, bins=bins, density=True)
        q, _ = np.histogram(sig2, bins=bins, density=True)
        p = p + 1e-5
        q = q + 1e-5
        p /= np.sum(p)
        q /= np.sum(q)
        return float(np.sum(p * np.log(p / q)))
        
    kl_no_bandpass = compute_kl(cases["A_Synth_NoBandpass"], cases["C_Real_NoBandpass"])
    kl_bandpass = compute_kl(cases["B_Synth_Bandpass"], cases["D_Real_Bandpass"])
    
    report = {
        "results": results,
        "kl_divergence": {
            "No_Bandpass_Synth_vs_Real": kl_no_bandpass,
            "Bandpass_Synth_vs_Real": kl_bandpass
        },
        "activations": activation_stats
    }
    
    with open(os.path.join(out_dir, "results.json"), "w") as f:
        json.dump(report, f, indent=4)
        
    print("Experiments completed successfully.")

if __name__ == '__main__':
    run_experiment()
