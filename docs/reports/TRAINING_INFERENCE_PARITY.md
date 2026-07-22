# Training vs Inference Parity Mismatches

| Stage | Training (`train_rppg_v2.py`) | Inference (`rppg_detector.py`) | Parity |
| :--- | :--- | :--- | :--- |
| **ROI** | `[int(h * 0.35):int(h * 0.65), int(w * 0.35):int(w * 0.65)]` | `[y1 + int(box_h * 0.50):y1 + int(box_h * 0.75), x1 + int(box_w * 0.60):x1 + int(box_w * 0.80)]` (when bbox is provided) or `[int(h * 0.45):int(h * 0.55), int(w * 0.45):int(w * 0.55)]` (when bbox is None) | **MISMATCH** |
| **Filtering** | None. Signal is NOT filtered (only noise added synthetically). | 2nd order Butterworth bandpass filter (0.7-4.0 Hz) applied using `scipy.signal.filtfilt`. | **CRITICAL MISMATCH** |
| **Detrending** | None directly prior to z-score standardization. | Mean subtraction (detrending) is computed, but `filtfilt` is erroneously applied to `sig_raw` (which has a huge DC offset) rather than `detrended`. | **CRITICAL MISMATCH** |
| **Normalization** | Standard Z-score normalization: `(signal - mean) / (std + 1e-6)` | Standard Z-score normalization: `(sig - mean) / (std + 1e-6)` | MATCH |
| **Tensor shape** | `(1, 1, 150)` | `(1, 1, 150)` | MATCH |
| **Tensor dtype** | `float32` | `float32` | MATCH |
| **Window size** | 150 frames (5s @ 30fps) | 150 frames | MATCH |

### Mismatch Analysis

1. **Filtering Parity**: The training data (both synthetic and video) does not undergo any bandpass filtering. However, the inference pipeline applies a 2nd order Butterworth bandpass filter (`filtfilt`). This means the model was trained on broadband signal characteristics (including noise) but receives narrowband filtered signals during inference.
2. **DC Offset Bug in Inference**: In `rppg_detector.py`, the Butterworth filter is applied to `sig_raw` instead of `detrended` (mean subtracted signal). Since the raw green channel has a massive DC offset (e.g., mean ~128), applying `filtfilt` directly to it causes severe edge ringing artifacts and numerical instability (values blowing up) at the boundaries of the 150-frame window. This distorted signal is then z-score normalized and fed to the model, leading to garbage outputs.
3. **ROI Parity**: The training script extracts a fixed center region `[0.35:0.65, 0.35:0.65]`. The inference pipeline extracts a different relative bounding box based on a face detector `[0.50:0.75, 0.60:0.80]` (which targets the cheek, but is misaligned with the training assumption).
