# PR-010 PIPELINE AUDIT

## 1. Camera Capture
* **Inputs:** Local hardware video stream / WebRTC
* **Outputs:** Encoded H264 bitstream (Annex-B format via WebCodecs)
* **Tensor Shape:** N/A (Raw byte chunks)
* **DType:** `Uint8Array` / `bytes`
* **Latency:** ~5-15ms (Encoding)
* **Confidence:** N/A
* **Failure Modes:** Camera permission denied, unsupported codec, dropped frames due to network congestion, hardware encoder failures on weak devices.

## 2. Face Detection (YOLO/MediaPipe)
* **Inputs:** Decoded RGB Frame (NumPy array)
* **Outputs:** Facial bounding box coordinates `[x1, y1, x2, y2]`
* **Tensor Shape:** `(H, W, 3)` -> BBox `(4,)`
* **DType:** `uint8` -> `int`
* **Latency:** ~10-25ms
* **Confidence:** 0.0 - 1.0 (BBox confidence)
* **Failure Modes:** Missed face under extreme angles, false positives on background patterns, detection failure due to heavy occlusion (e.g., 2D mask).

## 3. ROI Extraction
* **Inputs:** RGB Frame, BBox coordinates
* **Outputs:** Cropped spatial region (Forehead/Cheeks)
* **Tensor Shape:** `(ROI_H, ROI_W, 3)` (e.g., typically `(40, 25, 3)`)
* **DType:** `uint8`
* **Latency:** ~1-2ms
* **Confidence:** N/A
* **Failure Modes:** BBox jitter causing spatial inconsistencies over time, ROI drifting onto background, ROI cropping out of frame bounds.

## 4. Behavioral Inference
* **Inputs:** RGB Frame
* **Outputs:** Blink detection boolean, Head pose dictionary (yaw, pitch, roll)
* **Tensor Shape:** `(478, 3)` (Facial Landmarks)
* **DType:** `float32`
* **Latency:** ~15-30ms
* **Confidence:** Implicit in landmark geometry logic
* **Failure Modes:** Rapid movement causing landmark tracking loss, false blink detection due to lighting changes, incorrect pose angles on extreme rotations.

## 5. Anti-Spoof Inference (Spatial Model)
* **Inputs:** Cropped RGB Face Image
* **Outputs:** Probability of being Live
* **Tensor Shape:** `(1, 3, 224, 224)` or `(1, 3, 256, 256)` (depending on YOLO-cls architecture)
* **DType:** `float32`
* **Latency:** ~30-50ms
* **Confidence:** 0.0 - 1.0
* **Failure Modes:** Susceptible to high-fidelity video replay (tablet/iPad), false positives on deepfakes, false negatives on heavily compressed live video.

## 6. rPPG Inference (Temporal Model)
* **Inputs:** 150-frame buffer of spatially averaged ROI signals
* **Outputs:** Liveness score (derived from pulse extraction)
* **Tensor Shape:** `(1, 1, 150)`
* **DType:** `float32`
* **Latency:** ~20-40ms (Inference) + 5.0s (Initial Buffer Collection)
* **Confidence:** 0.0 - 1.0
* **Failure Modes:** Motion artifacts injecting physiological noise, false positives on video replays containing a valid pulse, filter failure if `scipy` is missing, variable sampling rate (FPS drops) ruining temporal consistency.

## 7. Fusion
* **Inputs:** Anti-Spoof score (`float`), rPPG score (`float`), Behavioral parameters, Challenge parameters
* **Outputs:** Combined Final Score, Final Verdict
* **Tensor Shape:** N/A (Scalars)
* **DType:** `float`
* **Latency:** < 1ms
* **Confidence:** 0.0 - 1.0
* **Failure Modes:** Weights not statistically optimized (e.g., `0.6` / `0.4`), fixed threshold (`0.5`) failing to account for variance in individual modalities, rigid challenge weights overriding otherwise confident signals.

## 8. Verdict
* **Inputs:** Combined Final Score
* **Outputs:** `Live` or `Spoof` string
* **Failure Modes:** Binarization loses confidence nuance, preventing downstream systems from demanding a step-up authentication.
