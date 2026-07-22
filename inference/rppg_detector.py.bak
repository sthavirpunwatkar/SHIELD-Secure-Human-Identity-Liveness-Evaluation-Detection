"""
inference/rppg_detector.py
===========================
Real-time rPPG liveness detector.

Model priority
--------------
1. models/rppg_1dcnn_v2.onnx (ONNX exported fast inference)
2. models/rppg_1dcnn_v2.pt  (upgraded dual-branch architecture)
3. models/rppg_1dcnn_v1.pt  (legacy simple CNN — backward compatible)

If no file exists the detector will raise a RuntimeError on update().
"""

from __future__ import annotations

import os
import sys

import cv2
import numpy as np
import torch
import torch.nn as nn

# ── make repo root importable ─────────────────────────────────────────────
_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)


# ---------------------------------------------------------------------------
# Legacy v1 architecture (kept for backward-compat weight loading)
# ---------------------------------------------------------------------------

def _build_v1_model() -> nn.Sequential:
    """Rebuild the original 2-conv simple 1D-CNN."""
    return nn.Sequential(
        nn.Conv1d(1, 16, kernel_size=3, padding=1),
        nn.ReLU(),
        nn.MaxPool1d(2),
        nn.Conv1d(16, 32, kernel_size=3, padding=1),
        nn.ReLU(),
        nn.AdaptiveAvgPool1d(1),
        nn.Flatten(),
        nn.Linear(32, 1),
        nn.Sigmoid(),
    )


# ---------------------------------------------------------------------------
# Detector class
# ---------------------------------------------------------------------------

class RPPGDetector:
    """
    Frame-by-frame rPPG liveness scorer.

    Parameters
    ----------
    window_size : int
        Number of consecutive frames that form one inference window.
        Default is 150 (≈ 5 s at 30 fps), matching the v2 training config.
    model_path : str | None
        Explicit path to .pt or .onnx weights.
    """

    # model variant constants
    _V2_INT8 = "models/rppg_1dcnn_v2_int8.onnx"
    _V2_ONNX = "models/rppg_1dcnn_v2.onnx"
    _V2_DEFAULT = "models/rppg_1dcnn_v2.pt"
    _V1_DEFAULT = "models/rppg_1dcnn_v1.pt"

    def __init__(
        self,
        window_size: int = 150,
        model_path: str | None = None,
    ) -> None:
        self.window_size   = window_size
        self.signal_buffer: list[float] = []
        self.device        = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.weights_loaded = False
        self._model_variant = "none"   # "v2_onnx", "v2", "v1", or "none"
        self.is_onnx = False
        self.session = None
        self.model = None

        # Determine which weights to load
        paths_to_try: list[tuple[str, str]] = []
        if model_path:
            # Explicit path
            if model_path.endswith('.onnx'):
                paths_to_try = [(model_path, "v2_onnx")]
            else:
                paths_to_try = [(model_path, "v2"), (model_path, "v1")]
        else:
            paths_to_try = [
                (self._V2_INT8, "v2_onnx"),
                (self._V2_ONNX, "v2_onnx"),
                (self._V2_DEFAULT, "v2"),
                (self._V1_DEFAULT, "v1"),
            ]

        self._load_weights(paths_to_try)

    # ── weight loading ────────────────────────────────────────────────────

    def _load_weights(self, candidates: list[tuple[str, str]]):
        """
        Try each (path, variant) candidate in order.  Return the first that
        loads successfully.  Falls back to mock mode if all fail.
        """
        for path, variant in candidates:
            if not os.path.exists(path):
                print(f"RPPGDetector: {path} not found – skipping.")
                continue

            try:
                if 'onnx' in variant:
                    import onnxruntime as ort
                    providers = ['CUDAExecutionProvider', 'CPUExecutionProvider']
                    self.session = ort.InferenceSession(path, providers=providers)
                    self.input_name = self.session.get_inputs()[0].name
                    self.output_name = self.session.get_outputs()[0].name
                    self.is_onnx = True
                else:
                    self.model = self._build_model(variant)
                    state = torch.load(path, map_location=self.device)
                    self.model.load_state_dict(state)
                    self.model.to(self.device)
                    self.model.eval()

                print(f"RPPGDetector: Loaded {variant} weights from {path}")
                self.weights_loaded  = True
                self._model_variant  = variant
                return
            except Exception as exc:
                print(f"RPPGDetector: Failed to load {path} as {variant}: {exc}")

        # No weights loaded - print warning and rely on update() to raise exception
        print("RPPGDetector: No valid weights found. Weights not loaded.")
        return

    def _build_model(self, variant: str) -> nn.Module:
        """Return the architecture matching *variant*."""
        if variant == "v2":
            try:
                from training.models.rppg_cnn import build_rppg_model_v2
                return build_rppg_model_v2(window_size=self.window_size)
            except ImportError as e:
                print(f"RPPGDetector: Cannot import v2 model ({e}). Using v1 arch.")
                return _build_v1_model()
        else:
            return _build_v1_model()

    # ── signal extraction ─────────────────────────────────────────────────

    def extract_roi_signal(self, frame: np.ndarray, bbox=None) -> float:
        import time
        if not hasattr(self, '_frame_counter'):
            self._frame_counter = 0
            self._start_time = time.time()
        self._frame_counter += 1
        
        print("\n" + "-"*56)
        print("ROI statistics")
        print(f"Frame Number: {self._frame_counter}")
        
        if not hasattr(self, '_saved_debug'):
            self._saved_debug = False
            import os
            os.makedirs("debug", exist_ok=True)
        
        if bbox is not None and len(bbox) == 4:
            x1, y1, x2, y2 = bbox
            h, w = frame.shape[:2]
            
            x1, y1 = max(0, int(x1)), max(0, int(y1))
            x2, y2 = min(w, int(x2)), min(h, int(y2))
            
            box_h = y2 - y1
            box_w = x2 - x1
            
            if box_h > 0 and box_w > 0:
                roi_y1 = y1 + int(box_h * 0.50)
                roi_y2 = y1 + int(box_h * 0.75)
                roi_x1 = x1 + int(box_w * 0.60)
                roi_x2 = x1 + int(box_w * 0.80)
                roi = frame[roi_y1:roi_y2, roi_x1:roi_x2]
            else:
                roi = np.array([])
        else:
            h, w = frame.shape[:2]
            y0, y1 = int(h * 0.45), int(h * 0.55)
            x0, x1 = int(w * 0.45), int(w * 0.55)
            roi = frame[y0:y1, x0:x1]
            
        if roi.size == 0:
            print("ROI width: 0")
            print("ROI height: 0")
            print("ROI mean RGB: [0, 0, 0]")
            print("ROI std RGB: [0, 0, 0]")
            print("ROI pixel count: 0")
            return 0.0
            
        print(f"ROI width: {roi.shape[1]}")
        print(f"ROI height: {roi.shape[0]}")
        print(f"ROI mean RGB: [{roi[:,:,2].mean():.2f}, {roi[:,:,1].mean():.2f}, {roi[:,:,0].mean():.2f}]") # OpenCV is BGR
        print(f"ROI std RGB: [{roi[:,:,2].std():.2f}, {roi[:,:,1].std():.2f}, {roi[:,:,0].std():.2f}]")
        print(f"ROI pixel count: {roi.shape[0] * roi.shape[1]}")
            
        if self._frame_counter % 30 == 0 and self._frame_counter <= 150:
            import cv2
            cv2.imwrite(f"debug/roi_frame_{self._frame_counter}.png", roi)

            
        return float(np.mean(roi[:, :, 1]))

    def update(self, frame: np.ndarray, bbox=None) -> float:
        val = self.extract_roi_signal(frame, bbox=bbox)
        self.signal_buffer.append(val)

        if len(self.signal_buffer) > self.window_size:
            self.signal_buffer.pop(0)
            
        import time
        elapsed = time.time() - getattr(self, '_start_time', time.time())
        est_fps = self._frame_counter / elapsed if elapsed > 0 else 30.0
        
        print("-" * 56)
        print("Signal Buffer")
        print(f"Current buffer length: {len(self.signal_buffer)}")
        print(f"Required length: {self.window_size}")
        print(f"Estimated runtime FPS: {est_fps:.2f}")
        print(f"Window duration: {len(self.signal_buffer) / 30.0:.2f}s") # hardcoded fps in pipeline

        if len(self.signal_buffer) < self.window_size:
            return 0.0

        if not self.weights_loaded:
            raise RuntimeError("RPPGDetector: weights not loaded.")

        sig_raw = np.array(self.signal_buffer, dtype=np.float32)
        
        raw_mean = sig_raw.mean()
        raw_std = sig_raw.std()
        
        detrended = sig_raw - raw_mean
        detrended_mean = detrended.mean()
        detrended_std = detrended.std()
        
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
            
        bandpass_mean = sig_bandpass.mean()
        bandpass_std = sig_bandpass.std()
        
        print("-" * 56)
        print("Preprocessing")
        print(f"Raw signal mean: {raw_mean:.6f}")
        print(f"Raw signal std: {raw_std:.6f}")
        print(f"Detrended signal mean: {detrended_mean:.6f}")
        print(f"Detrended signal std: {detrended_std:.6f}")
        print(f"Bandpass output mean: {bandpass_mean:.6f}")
        print(f"Bandpass output std: {bandpass_std:.6f}")
        print(f"Min: {sig_bandpass.min():.6f}")
        print(f"Max: {sig_bandpass.max():.6f}")
        
        # Frequency analysis
        fft = np.abs(np.fft.rfft(sig_bandpass))
        freqs = np.fft.rfftfreq(len(sig_bandpass), 1.0/30.0)
        
        valid_idx = np.where((freqs >= 0.7) & (freqs <= 4.0))[0]
        if len(valid_idx) > 0:
            dom_idx = valid_idx[np.argmax(fft[valid_idx])]
            dom_freq = freqs[dom_idx]
            est_bpm = dom_freq * 60
            peak_mag = fft[dom_idx]
            snr = peak_mag / (np.sum(fft[valid_idx]) - peak_mag + 1e-6)
        else:
            dom_freq = 0
            est_bpm = 0
            peak_mag = 0
            snr = 0
            
        print("-" * 56)
        print("Frequency Analysis")
        print(f"Dominant frequency: {dom_freq:.2f} Hz")
        print(f"Estimated BPM: {est_bpm:.1f}")
        print(f"FFT peak magnitude: {peak_mag:.2f}")
        print(f"Signal-to-noise ratio: {snr:.4f}")
            
        sig = sig_bandpass.astype(np.float32)
        sig = (sig - sig.mean()) / (sig.std() + 1e-6)

        if len(self.signal_buffer) == self.window_size and not self._saved_debug:
            self._saved_debug = True
            np.savetxt("debug/raw_signal.csv", sig_raw, delimiter=",")
            np.savetxt("debug/detrended_signal.csv", detrended, delimiter=",")
            np.savetxt("debug/bandpassed_signal.csv", sig_bandpass, delimiter=",")
            np.savetxt("debug/model_input.csv", sig, delimiter=",")

        print("-" * 56)
        print("ONNX Input")
        tensor_shape = (1, 1, self.window_size)
        print(f"Tensor shape: {tensor_shape}")
        print(f"Tensor dtype: {sig.dtype}")
        print(f"Tensor min: {sig.min():.4f}")
        print(f"Tensor max: {sig.max():.4f}")
        print(f"Tensor mean: {sig.mean():.4f}")
        print(f"Tensor std: {sig.std():.4f}")

        if self.is_onnx:
            sig = np.expand_dims(np.expand_dims(sig, axis=0), axis=0)
            outputs = self.session.run([self.output_name], {self.input_name: sig})[0]
            score = float(outputs[0][0])
        else:
            tensor = torch.from_numpy(sig).unsqueeze(0).unsqueeze(0).to(self.device)
            with torch.no_grad():
                score = self.model(tensor).item()

        print("-" * 56)
        print("ONNX Output")
        print(f"Raw logits: N/A (Model includes Sigmoid)")
        print(f"Sigmoid output: {score:.6f}")
        print(f"Final rPPG score: {score:.6f}")
        
        return score

    # ── convenience ───────────────────────────────────────────────────────

    def reset(self) -> None:
        """Clear the signal buffer (e.g. between subjects)."""
        self.signal_buffer.clear()

    @property
    def buffer_fill(self) -> float:
        """Fraction of the window that is currently filled [0, 1]."""
        return len(self.signal_buffer) / self.window_size


# ---------------------------------------------------------------------------
# Quick smoke-test
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    detector = RPPGDetector()
    dummy    = np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)

    for i in range(155):
        score = detector.update(dummy)

    print(f"RPPGDetector OK  variant={detector._model_variant!r}  "
          f"score={score:.4f}  window={detector.window_size}")
