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

    def extract_roi_signal(self, frame: np.ndarray, landmarks=None) -> float:
        """
        Extract the average green-channel value from the centre-10% crop of
        *frame* (a proxy for the facial skin ROI).
        """
        h, w = frame.shape[:2]
        y0, y1 = int(h * 0.45), int(h * 0.55)
        x0, x1 = int(w * 0.45), int(w * 0.55)
        roi = frame[y0:y1, x0:x1]
        if roi.size == 0:
            return 0.0
        return float(np.mean(roi[:, :, 1]))

    # ── frame update ──────────────────────────────────────────────────────

    def update(self, frame: np.ndarray) -> float:
        """
        Ingest one frame and return a liveness probability.
        """
        self.signal_buffer.append(self.extract_roi_signal(frame))

        # Rolling window — drop oldest sample when over-full
        if len(self.signal_buffer) > self.window_size:
            self.signal_buffer.pop(0)

        if len(self.signal_buffer) < self.window_size:
            return 0.5   # not enough data yet

        if not self.weights_loaded:
            raise RuntimeError("RPPGDetector: weights not loaded.")

        # Normalise & run inference
        sig = np.array(self.signal_buffer, dtype=np.float32)
        sig = (sig - sig.mean()) / (sig.std() + 1e-6)

        if self.is_onnx:
            sig = np.expand_dims(np.expand_dims(sig, axis=0), axis=0) # [1, 1, T]
            outputs = self.session.run([self.output_name], {self.input_name: sig})[0]
            return float(outputs[0][0])

        tensor = torch.from_numpy(sig).unsqueeze(0).unsqueeze(0).to(self.device)  # (1,1,T)
        with torch.no_grad():
            score = self.model(tensor).item()

        return float(score)

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
