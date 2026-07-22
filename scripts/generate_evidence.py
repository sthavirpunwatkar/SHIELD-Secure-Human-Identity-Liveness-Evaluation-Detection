import sys
import os
import time
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import cv2

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from inference.rppg_detector import RPPGDetector

# Setup directories
os.makedirs("debug/images", exist_ok=True)
os.makedirs("debug", exist_ok=True)

pipeline_trace = []
temporal_data = []

class TracedRPPGDetector(RPPGDetector):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.frame_timestamps = []
        self.frame_number = 0
        self.stage_times = {}

    def extract_roi_signal(self, frame: np.ndarray, bbox=None) -> float:
        t0 = time.time()
        self.frame_number += 1
        
        # Original Frame
        if self.frame_number == 150:
            cv2.imwrite("debug/images/original_frame.png", frame)
            if bbox is not None:
                img_bbox = frame.copy()
                x1, y1, x2, y2 = bbox
                cv2.rectangle(img_bbox, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.imwrite("debug/images/bounding_boxes.png", img_bbox)
        
        val = super().extract_roi_signal(frame, bbox)
        
        t1 = time.time()
        self._record_stage("ROI_Extraction", np.array([val]), t1 - t0)
        return val

    def update(self, frame: np.ndarray, bbox=None) -> float:
        t_start = time.time()
        
        # Track timing
        self.frame_timestamps.append(time.time())
        if len(self.frame_timestamps) > self.window_size:
            self.frame_timestamps.pop(0)
            
        val = self.extract_roi_signal(frame, bbox=bbox)
        self.signal_buffer.append(val)

        if len(self.signal_buffer) > self.window_size:
            self.signal_buffer.pop(0)

        if len(self.signal_buffer) < self.window_size:
            temporal_data.append({
                "frame": self.frame_number,
                "confidence": 0.0,
                "buffer_fill": len(self.signal_buffer),
                "latency": time.time() - t_start,
                "variance": 0.0
            })
            return 0.0

        if not self.weights_loaded:
            raise RuntimeError("RPPGDetector: weights not loaded.")

        # STAGE: Raw Signal
        t0 = time.time()
        sig_raw = np.array(self.signal_buffer, dtype=np.float32)
        raw_mean = sig_raw.mean()
        raw_std = sig_raw.std()
        t1 = time.time()
        self._record_stage("Raw_Signal", sig_raw, t1 - t0)

        # STAGE: Detrended Signal
        t0 = time.time()
        detrended = sig_raw - raw_mean
        t1 = time.time()
        self._record_stage("Detrended_Signal", detrended, t1 - t0)

        # STAGE: Filtering
        t0 = time.time()
        try:
            from scipy.signal import butter, filtfilt
            fps = 30.0
            nyq = 0.5 * fps
            low = 0.7 / nyq
            high = 4.0 / nyq
            b, a = butter(2, [low, high], btype='band')
            sig_bandpass = filtfilt(b, a, sig_raw)
        except ImportError:
            sig_bandpass = detrended
        t1 = time.time()
        self._record_stage("Bandpass_Signal", sig_bandpass, t1 - t0)

        # STAGE: Normalization
        t0 = time.time()
        sig = sig_bandpass.astype(np.float32)
        sig = (sig - sig.mean()) / (sig.std() + 1e-6)
        t1 = time.time()
        self._record_stage("Normalized_Signal", sig, t1 - t0)

        # Save signals for plotting on frame 150
        if self.frame_number == 150:
            np.savetxt("debug/raw_signal.csv", sig_raw, delimiter=",")
            np.savetxt("debug/detrended_signal.csv", detrended, delimiter=",")
            np.savetxt("debug/bandpassed_signal.csv", sig_bandpass, delimiter=",")
            np.savetxt("debug/model_input.csv", sig, delimiter=",")
            
            plt.figure(figsize=(10, 8))
            plt.subplot(4, 1, 1)
            plt.plot(sig_raw)
            plt.title("Raw Signal")
            plt.subplot(4, 1, 2)
            plt.plot(detrended)
            plt.title("Detrended Signal")
            plt.subplot(4, 1, 3)
            plt.plot(sig_bandpass)
            plt.title("Bandpassed Signal (Notice the ringing from DC offset!)")
            plt.subplot(4, 1, 4)
            plt.plot(sig)
            plt.title("Normalized Signal (Model Input)")
            plt.tight_layout()
            plt.savefig("debug/signal_validation.png")
            
            # PHASE 7: Dump input tensor
            np.save("debug/input_tensor.npy", sig)
            with open("debug/input_tensor_stats.json", "w") as f:
                json.dump({
                    "shape": list(sig.shape),
                    "dtype": str(sig.dtype),
                    "min": float(np.min(sig)),
                    "max": float(np.max(sig)),
                    "mean": float(np.mean(sig)),
                    "std": float(np.std(sig)),
                    "nan_count": int(np.isnan(sig).sum()),
                    "inf_count": int(np.isinf(sig).sum())
                }, f, indent=4)

        # Model Inference
        t0 = time.time()
        import torch
        if self.is_onnx:
            sig_input = np.expand_dims(np.expand_dims(sig, axis=0), axis=0)
            outputs = self.session.run([self.output_name], {self.input_name: sig_input})[0]
            raw_out = outputs[0]
            score = float(outputs[0][0])
        else:
            tensor = torch.from_numpy(sig).unsqueeze(0).unsqueeze(0).to(self.device)
            with torch.no_grad():
                outputs = self.model(tensor)
                raw_out = outputs.cpu().numpy()
                score = outputs.item()
        t1 = time.time()
        self._record_stage("Model_Inference_Raw_Output", raw_out, t1 - t0)

        # STAGE: Confidence Score
        self._record_stage("Confidence_Score", np.array([score]), 0)

        if self.frame_number == 150:
            np.save("debug/raw_output.npy", raw_out)

        temporal_data.append({
            "frame": self.frame_number,
            "confidence": score,
            "buffer_fill": len(self.signal_buffer),
            "latency": time.time() - t_start,
            "variance": float(np.var(sig_raw))
        })
        
        return score

    def _record_stage(self, name, data, duration):
        pipeline_trace.append({
            "frame": self.frame_number,
            "stage": name,
            "shape": str(data.shape),
            "dtype": str(data.dtype),
            "min": float(np.min(data)),
            "max": float(np.max(data)),
            "mean": float(np.mean(data)),
            "std": float(np.std(data)),
            "nan_count": int(np.isnan(data).sum()),
            "inf_count": int(np.isinf(data).sum()),
            "processing_time_ms": duration * 1000.0
        })

def create_synthetic_frame(val, frame_idx):
    frame = np.full((480, 640, 3), [100, 150, 200], dtype=np.float32)
    # Add face rect
    cv2.rectangle(frame, (100, 100), (440, 340), (120, val, 210), -1)
    frame[:, :, 1] += val # Inject signal to green channel
    return np.clip(frame, 0, 255).astype(np.uint8)

def run():
    print("Running Controlled Experiment: Synthetic Sinusoidal Signal")
    detector = TracedRPPGDetector(window_size=150)
    
    # Generate clean sinusoidal signal (similar to live human)
    t = np.linspace(0, 150/30.0, 150)
    signal = 128 + 5.0 * np.sin(2 * np.pi * 1.5 * t)
    
    bbox = [100, 100, 440, 340]
    
    for i in range(160):
        val = signal[i] if i < 150 else signal[-1]
        frame = create_synthetic_frame(val, i)
        detector.update(frame, bbox=bbox)
        
    df_trace = pd.DataFrame(pipeline_trace)
    df_trace.to_csv("pipeline_trace.csv", index=False)
    
    df_temp = pd.DataFrame(temporal_data)
    
    plt.figure(figsize=(10, 5))
    plt.plot(df_temp["frame"], df_temp["confidence"], marker='o')
    plt.title("Confidence vs Frame Number")
    plt.xlabel("Frame")
    plt.ylabel("Confidence")
    plt.grid(True)
    plt.savefig("debug/temporal_analysis.png")
    
    print("Evidence generation complete.")

if __name__ == "__main__":
    run()
