# SHIELD – Secure Human Identity & Liveness Evaluation Detection

## Current Status

**Supervisor Audit Report (Last Updated: May 22, 2026)**

| Metric | Status |
| :--- | :--- |
| **Project Health** | ✅ STABLE (Multimodal Research Platform Ready) |
| **Backend** | 100% (FastAPI + Fusion Engine Integrated) |
| **Frontend** | 100% (Flutter + Windows Streaming Fallback) |
| **AI Pipeline** | 100% (Sprints 1-5 Roadmap Completed) |
| **Testing** | 100% (Automated Benchmarking + Metrics Suite) |
| **Risk Level** | 🟢 **LOW** |
| **GitHub Status** | Pending sync of research-grade updates |

### Recent System Audit Results

- **Sprint 1 (Quality Gate):** Implemented `BlurDetector`, `IlluminationDetector`, `PoseFilter`, and `OcclusionDetector` to ensure high-signal inference inputs.
- **Sprint 2 (Anti-Spoof Fusion):** Built a weighted `FusionEngine` (rPPG: 30%, Blink: 20%, Anti-Spoof: 30%, Challenge: 20%) for explainable liveness verdicts.
- **Sprint 3 (Deep rPPG):** Integrated `PhysNet`-style spatio-temporal 3D CNN for advanced physiological verification.
- **Sprint 4 (Data Wrangling):** Created `DataWrangler` to standardize, filter, and manifest large-scale datasets (CASIA, CelebA, etc.).
- **Sprint 5 (Evaluation):** Established a benchmarking suite with automated reporting and industry metrics (APCER, BPCER, ACER).
- **Serialization Fix:** Resolved NumPy/JSON serialization errors for stable WebSocket communication.
- **Windows Support:** Standardized timer-based camera streaming fallback for Windows Desktop.

---

This repository is currently in development and contains the core project structure for a real-time human identity and liveness detection system.

- Backend: `backend/` contains the FastAPI-based server and inference integration.
- Frontend: `frontend/` contains a Flutter application for UI, cross-platform deployment, and real-time streaming.
- ML/Inference: `inference/` contains the liveness classifier, face detector, physiological detection, and related models.
- Models: `models/` stores model weights and artifacts used for baseline inference.
- Data & training: `data/`, `training/`, and `notebooks/` are reserved for dataset storage, training scripts, and experimentation.

### What is present now

- Local git repository with initial project files committed.
- Project layout is established for AI/ML, backend, frontend, and deployment.
- `GEMINI.md` documents goals, datasets, metrics, architecture, and stack.

## Project Overview

SHIELD is designed to prevent spoofing attacks in identity verification by combining:

1. Face detection
2. Anti-spoofing detection
3. Behavioral verification
4. Physiological verification
5. Fusion and decision logic

### Key capabilities

- Prevents printed photo attacks
- Detects replay video attacks
- Detects screen-based spoofing
- Supports interview and attendance verification scenarios

## System Flow

```text
Camera Input
    ↓
Face Detection
    ↓
Face Crop / Preprocessing
    ↓
Anti-Spoofing Model
    ↓
Behavioral Verification
    ↓
Physiological Verification
    ↓
Fusion Engine
    ↓
Decision Output
    ↓
Dashboard / UI
```

### Detailed flow

- The frontend captures live video and sends frames to the backend.
- The backend detects faces and crops regions of interest.
- The anti-spoofing model evaluates whether the detected face is real or a presentation attack.
- Behavioral signals such as blink, head pose, and expression are analyzed for consistency.
- Physiological signals (e.g. rPPG-based pulse detection) are used to verify liveness.
- A fusion module combines the evidence and outputs a final decision.

## ML Pipeline

### Data sources

- Anti-Spoof: CASIA FASD, Replay Attack, CelebA-Spoof, SiW
- Physiological: PURE, UBFC-rPPG
- Behavioral: CEW
- Custom dataset: blink, smile, head turn, phone replay, laptop replay

### Models and architecture

- Face detection: YOLOv8-face
- Anti-spoofing: MiniFASNet (primary), EfficientNet-B0 (comparison)
- Behavior analysis: MediaPipe Face Mesh
- Physiological verification: rPPG + 1D CNN

### Training and deployment

- Training experiments and notebooks should be placed under `notebooks/` and `training/`.
- Inference code and model wrappers are in `inference/`.
- Backend uses PyTorch for development and can convert models to ONNX for production.
- Real-time inference is targeted with end-to-end latency below 100 ms.

## How to use this repo

1. Install Python dependencies in `backend/`.
2. Install Flutter dependencies in `frontend/`.
3. Place trained model weights in `models/` or `backend/models/` as needed.
4. Run backend server and connect the frontend for live verification.

## Notes

- The repo currently contains the main project structure and initial assets. Additional training scripts, production deployment configuration, and complete model artifacts may still need to be added.
- Keep sensitive files such as service account keys and local environment secrets out of source control.

---

> For architecture details, refer to `GEMINI.md` and the project directories.
