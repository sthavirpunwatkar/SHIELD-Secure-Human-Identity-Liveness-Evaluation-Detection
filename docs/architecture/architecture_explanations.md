# SHIELD Architecture - Explanations

## Overview
SHIELD (Secure Human Identity Evaluation and Liveness Detection) is designed as a highly scalable, real-time liveness detection and anti-spoofing system. It bridges a Flutter-based client capturing optimized video frames, streaming them over a low-latency WebSocket connection to a FastAPI python backend.

## 1. Frontend Architecture
The Flutter frontend consists of three primary screens and several services.
- **CameraCaptureService** utilizes platform channels to grab raw camera frames at 30 FPS.
- **WebCodecs (or stub)** compresses these frames into H.264 chunks.
- **FrameTransportService** maintains a bounded queue (max 30 frames) to manage network backpressure and sends these bytes interlaced with JSON metadata over WebSockets.
- **ChallengeService** parses backend commands, runs local UI countdowns, and emits state changes.

## 2. Backend & Communication
- **WebSockets** are used because HTTP overhead per frame would destroy latency.
- The connection requires SEB (Safe Exam Browser) cryptographic headers, verified by `seb_service.py`.
- **StreamingDecoder** unpacks the H.264 chunks into raw `numpy` BGR arrays.

## 3. Inference Pipeline (The Cascade)
The backend does not run all models at once. It uses a strict cascade to exit early and save GPU/CPU cycles:
1. **YoloSegDetector**: Quickly finds the face bounding box and masks. If it sees a physical mask, it exits immediately (`Spoof`). If no face is found, it exits.
2. **QualityScoreEngine**: Checks brightness, blur, and contrast. If the frame is too dark or blurry, it drops the frame to prevent bad data from polluting the downstream models.
3. **BehavioralAnalyzer (MediaPipe)**: Extracts 468 landmarks. Computes EAR (Eye Aspect Ratio) for blinks, and PnP for head pose. If active challenges are running, it verifies the action (e.g., `nod`, `smile`).
4. **AntispoofInference (MiniFASNet)**: Analyzes the cropped face for printed/digital replays (moire patterns, screen borders). If this scores `< 0.25`, the cascade critically fails immediately.
5. **RPPGDetector**: Extracts the green channel signal from the forehead/cheeks across a sliding window buffer, estimating the presence of a live pulse.

## 4. Fusion Engine
The `FusionEngine` merges all these scores. 
- During a challenge, weights are distributed (`rPPG: 0.1, Behavior: 0.1, Appearance: 0.4, Challenge: 0.4`).
- During passive monitoring, challenge score drops to 0, and Appearance (`0.5`) and rPPG (`0.3`) take over.
- The system defaults to `Spoof` if the weighted sum falls below `0.5`.

## 5. Storage & Lifecycle
Every single session is assigned a UUID. Frame-by-frame data (latencies, confidence, verdicts) is appended to JSONL log files. The final summarized verdict is written to SQLite (`shield_local.db`). In demo modes, annotated debug images are saved to local storage.
