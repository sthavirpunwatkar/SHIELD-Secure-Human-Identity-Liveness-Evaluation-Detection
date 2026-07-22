import sys
import os
import time
import numpy as np
import torch
from scipy.signal import butter, filtfilt

sys.path.append(os.path.abspath(os.path.dirname(__file__)))
from inference.rppg_detector import RPPGDetector
from training.train_rppg_v2 import generate_live_signal
from inference.fusion_engine import FusionEngine

def create_frame(live_val, spoof_val, photo=False):
    h, w = 480, 640
    frame = np.random.randint(0, 255, (h, w, 3), dtype=np.uint8)
    
    # Draw a "face" in the center (bbox: x=160 to 480, y=100 to 380)
    face_y1, face_y2 = 100, 380
    face_x1, face_x2 = 160, 480
    
    # Base skin tone
    face_color = np.array([100, 150, 200], dtype=np.float32) # BGR
    
    # If photo, signal is static noise. If live, it has the pulse.
    # In both cases, only the "face" has the signal, background is random noise
    
    face_region = np.full((face_y2-face_y1, face_x2-face_x1, 3), face_color, dtype=np.float32)
    signal_val = spoof_val if photo else live_val
    face_region[:, :, 1] += signal_val * 10.0 # Inject signal into green channel
    
    frame[face_y1:face_y2, face_x1:face_x2] = np.clip(face_region, 0, 255).astype(np.uint8)
    
    return frame, [face_x1, face_y1, face_x2, face_y2]

class ParityDetector(RPPGDetector):
    def __init__(self, use_butterworth=True, match_training_roi=False):
        super().__init__(window_size=150)
        self.use_butterworth = use_butterworth
        self.match_training_roi = match_training_roi
        self.recorded_tensor = None
        
    def extract_roi_signal(self, frame: np.ndarray, bbox=None) -> float:
        if self.match_training_roi:
            h, w = frame.shape[:2]
            roi = frame[int(h * 0.35):int(h * 0.65), int(w * 0.35):int(w * 0.65)]
        else:
            if bbox is not None and len(bbox) == 4:
                x1, y1, x2, y2 = bbox
                h, w = frame.shape[:2]
                x1, y1 = max(0, int(x1)), max(0, int(y1))
                x2, y2 = min(w, int(x2)), min(h, int(y2))
                box_h = y2 - y1
                box_w = x2 - x1
                roi_y1 = y1 + int(box_h * 0.50)
                roi_y2 = y1 + int(box_h * 0.75)
                roi_x1 = x1 + int(box_w * 0.60)
                roi_x2 = x1 + int(box_w * 0.80)
                roi = frame[roi_y1:roi_y2, roi_x1:roi_x2]
            else:
                roi = np.array([])
                
        if roi.size == 0:
            return 0.0
        return float(np.mean(roi[:, :, 1]))
        
    def update(self, frame: np.ndarray, bbox=None) -> float:
        val = self.extract_roi_signal(frame, bbox=bbox)
        self.signal_buffer.append(val)

        if len(self.signal_buffer) > self.window_size:
            self.signal_buffer.pop(0)

        if len(self.signal_buffer) < self.window_size:
            return 0.0

        sig = np.array(self.signal_buffer, dtype=np.float32)
        
        if self.use_butterworth:
            fps = 30.0
            nyq = 0.5 * fps
            low = 0.7 / nyq
            high = 4.0 / nyq
            b, a = butter(2, [low, high], btype='band')
            sig = filtfilt(b, a, sig)
        else:
            sig = sig - sig.mean()
            
        sig = sig.astype(np.float32)
        sig = (sig - sig.mean()) / (sig.std() + 1e-6)

        self.recorded_tensor = sig.copy()

        if self.is_onnx:
            sig_input = np.expand_dims(np.expand_dims(sig, axis=0), axis=0)
            outputs = self.session.run([self.output_name], {self.input_name: sig_input})[0]
            return float(outputs[0][0])
        else:
            tensor = torch.from_numpy(sig).unsqueeze(0).unsqueeze(0).to(self.device)
            with torch.no_grad():
                score = self.model(tensor).item()
            return float(score)

def run_experiment(name, use_butterworth, match_training_roi):
    print(f"\n{'='*80}")
    print(f"EXPERIMENT: {name}")
    print(f"Butterworth: {use_butterworth} | Match Training ROI: {match_training_roi}")
    print(f"{'='*80}")
    
    live_sig = generate_live_signal(150, fps=30)
    spoof_sig = np.random.randn(150).astype(np.float32) * 0.01 
    
    engine = FusionEngine()
    
    for scenario_name, is_photo in [("Live Face", False), ("Printed Photo", True)]:
        detector = ParityDetector(use_butterworth=use_butterworth, match_training_roi=match_training_roi)
        
        score = 0.0
        for i in range(150):
            frame, bbox = create_frame(live_sig[i], spoof_sig[i], photo=is_photo)
            score = detector.update(frame, bbox=bbox)
            
        # Simulate other modalities for fusion
        blink_score = 0.0 if is_photo else 1.0
        antispoof_score = 0.75 if is_photo else 0.90
        
        fusion_res = engine.fuse(rppg_score=score, blink_score=blink_score, antispoof_score=antispoof_score)
        
        print(f"\n[{scenario_name}]")
        print(f"  rPPG Score   : {score:.6f}")
        print(f"  Fusion Score : {fusion_res['final_score']:.6f}")
        print(f"  Verdict      : {fusion_res['verdict']}")
        
        tensor = detector.recorded_tensor
        print(f"  Tensor stats : mean={tensor.mean():.4f}, std={tensor.std():.4f}, min={tensor.min():.4f}, max={tensor.max():.4f}")

if __name__ == "__main__":
    import warnings
    warnings.filterwarnings("ignore")
    # Exp A: Keep ROI unchanged (Runtime ROI), Disable Butterworth
    run_experiment("A", use_butterworth=False, match_training_roi=False)
    
    # Exp B: Restore Butterworth, Match Training ROI
    run_experiment("B", use_butterworth=True, match_training_roi=True)
    
    # Exp C: Apply Both (Disable Butterworth, Match Training ROI)
    run_experiment("C", use_butterworth=False, match_training_roi=True)
