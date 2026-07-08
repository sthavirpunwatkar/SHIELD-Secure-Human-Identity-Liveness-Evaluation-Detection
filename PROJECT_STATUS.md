# SHIELD Project Status

## Project Summary
SHIELD (Secure Human Identity & Liveness Evaluation Detection) is a production-ready multimodal biometric authentication system capable of detecting presentation attacks (spoofs, 2D replays, 3D masks) while maintaining high accuracy via a fusion of YOLOv8/MediaPipe (Face Detection), MiniFASNet (Anti-Spoofing), and a 1D-CNN rPPG Network (Physiological Liveness).

## Current Architecture
* **Frontend:** Flutter mobile app relying on a 2 FPS `takePicture()` throttling loop.
* **Backend:** FastAPI monolithic Python backend over WebSockets.
* **Database:** Synchronous SQLite database integrated directly into the async event loop.
* **Inference:** PyTorch / ONNX models loaded synchronously into memory.

## Current Version
**v1.0 (Frozen)**

## Verified Components
* YOLOv8 Face Detection Checkpoints.
* MediaPipe FaceLandmarker Pose/Mesh extraction.
* MiniFASNet Spoofer Detection.
* 1D-CNN rPPG dual-branch forward pass and expected tensor shapes.
* SEB (Safe Exam Browser) WebSocket Handshake validation.

## Completed Research
* **FPS Bottlenecks:** Traced capture latency; proved frontend operates at 2 FPS, mathematically breaking the 30 FPS rPPG requirement.
* **Database I/O:** Verified that synchronous SQLite writes block the FastAPI event loop, causing WebSocket drops.
* **Identity Yaw:** Confirmed Identity Signature fails when user head Yaw exceeds 10°.
* **Architecture Validation:** Disqualified on-device edge ML for zero-trust compliance.

## Completed Experiments
* **ROI Optimization Study:** Mapped 7 facial regions, concluding the right/left cheek produces the highest SNR (6.62 dB).
* **Parity Investigation:** Proved that training used a `0.7 - 4.0 Hz` bandpass filter while inference was fed raw noise.

## Implemented Features
* **rPPG ROI Fix:** Dynamically maps MediaPipe/YOLO face boundaries to isolated cheek regions.
* **Mathematical Parity:** Injected `scipy.signal.filtfilt` directly into `rppg_detector.py` to match the exact training distribution.

## Known Issues
1. `takePicture()` forces a 2 FPS stream, breaking the Nyquist limit for heart rate detection.
2. Synchronous DB calls crash concurrent WebSockets.
3. Identity Signature rejects legitimate users moving their heads.

## Known Risks
* Implementing WebRTC/H.264 streaming introduces significant backend decoding complexity (`aiortc` / FFmpeg).
* Refactoring the DB to `asyncpg`/`aiosqlite` requires widespread schema/session changes.

## Pending Milestones (Version 2)
1. Asynchronous Database Migration.
2. 3D Identity Signature Logic Refactor.
3. Backend H.264 Video Stream Decoding.
4. Frontend Native 30 FPS Streaming.

## Future Work
* Enterprise-grade horizontal scaling using Apache Kafka.
* Kubernetes deployment architecture.
* Dedicated GPU node scheduling.

## Current Progress Percentage
* **Version 1 (Audit & Preparation):** 100% Complete.
* **Version 2 (Implementation):** 0% Complete.
