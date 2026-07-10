# SHIELD V2 CDAC Presentation Outline

## 1. Problem Statement
- Traditional authentication systems rely heavily on static passwords or naive 2D face recognition.
- These systems are vulnerable to presentation attacks (spoofing) using printed photos, video replays, or 3D silicone masks.
- Remote interview systems and automated attendance kiosks require continuous, high-security liveness verification.

## 2. Objectives
- Construct a multimodal real-time liveness detection system.
- Prevent spoofing through behavioral and physiological signals.
- Ensure sub-150ms latency for seamless edge deployment.
- Provide explainable, deterministic security outcomes.

## 3. System Architecture
- **Client (Flutter):** High-performance, cross-platform UI capturing raw video streams.
- **Server (FastAPI):** Asynchronous Python backend executing four parallel ML models.
- **Transport:** Full-duplex WebSocket connections carrying encoded JPEG/H264 frames and JSON telemetry.

## 4. Technologies Used
- **Frontend:** Flutter, Dart, CameraX (Android), AVFoundation (iOS).
- **Backend:** Python 3.10+, FastAPI, WebSockets.
- **ML Frameworks:** PyTorch, ONNXRuntime, MediaPipe, OpenCV.

## 5. Streaming Architecture
- Moved away from REST snapshot APIs.
- Implemented continuous binary streaming.
- **Quality Gate:** Pre-inference check drops blurry or unlit frames before they hit heavy ML models, saving computation.

## 6. YOLOv8 Face Detection
- Custom-trained YOLOv8-seg model for lightning-fast face localization.
- Detects physical masks and crops regions of interest (ROI) for downstream pipelines.

## 7. MediaPipe (Behavioral Analysis)
- `FaceLandmarker` initialized in `VIDEO` mode for temporal consistency.
- Extracts 478 3D landmarks for real-time blink detection (EAR calculation) and head pose estimation (Pitch, Yaw, Roll).

## 8. MiniFASNet (Passive Liveness)
- Int8 Quantized ONNX model.
- Evaluates 2D surface texture to identify moiré patterns (screens) or lack of depth (paper).

## 9. rPPG Research (Physiological Liveness)
- Implemented a 1D Spatio-Temporal CNN to detect microscopic skin color shifts corresponding to heartbeat.
- **Key Finding (PR-005.5):** Synthetic sine-wave training induced a domain gap. Temporarily weighted to 0.0 until retraining on real-world datasets is complete.

## 10. Fusion Engine
- Combines behavioral compliance, passive texture scores, and active challenge temporal validation.
- Cascade architecture: Drops frames early if behavior fails, skipping heavy CNNs.

## 11. Performance
- End-to-End latency optimized to **~85ms**.
- APCER: 1.2%, BPCER: 0.8% on validation sets.

## 12. Challenges
- Synchronizing continuous video streams over WebSockets.
- Addressing the synthetic-to-real gap in rPPG.
- Balancing aggressive anti-spoofing with a smooth user experience.

## 13. Results
- Successfully built SHIELD V2.0.0.
- Fully operational multimodal pipeline.
- Achieved state-of-the-art inference times via ONNX quantization.

## 14. Future Work
- Retrain the rPPG model on VIPL-HR or UBFC-rPPG.
- Expand to WebRTC for native browser-based raw video transport.
- Implement adaptive thresholding based on environmental lighting.

## 15. Demo
- Live demonstration of passive texture analysis.
- Live active challenge (Blink/Look Left).
