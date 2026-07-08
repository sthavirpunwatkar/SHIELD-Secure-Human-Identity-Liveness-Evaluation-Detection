# Changelog

All notable changes to this project will be documented in this file.

## [v1.0] - 2026-07-08

### Verified Fixes
* **rPPG ROI Fix:** Dynamically maps MediaPipe/YOLO face boundaries to isolated cheek regions instead of a fixed, static center crop.
* **Mathematical Parity:** Injected `scipy.signal.filtfilt` bandpass filter directly into `inference/rppg_detector.py` to match the exact distribution the model was trained on, resolving the `0.0000` confidence crash.

### Investigations Completed
* **Database I/O Bottleneck:** Investigated and verified that synchronous SQLite calls block the FastAPI event loop, establishing the root cause for WebSocket disconnects.
* **Identity Signature Yaw Vulnerability:** Verified that the 2D geometric distance metric used in session management fails violently when head yaw exceeds 10 degrees.
* **FPS Bottleneck:** Traced the entire video pipeline to prove the frontend transmits at exactly 2 FPS, theoretically violating the Nyquist-Shannon limit for human pulse detection.

### Experiments Concluded
* **ROI Optimization Study:** Ran controlled studies across 7 facial regions. Measured SNR, Temporal Variance, and FFT Peak Quality. Established the right/left cheek as the optimal physical signal region.
* **Synthetic Sine Wave Injection:** Bypassed the spatial logic to inject pure 60/75/90/120 BPM sine waves directly into the 1D-CNN rPPG network to isolate training/inference normalization anomalies.

### Architectural Decisions
* **ADR Generated:** Finalized the architecture decision to deprecate `startImageStream` and `takePicture` in favor of **H.264 WebRTC/Chunk Streaming** for zero-trust security and exact 30 FPS temporal preservation.
