# SHIELD – Secure Human Identity & Liveness Evaluation Detection

## Project Type
AI/ML Final Year Project

Domains:
- Face Anti-Spoofing
- Liveness Detection
- Interview Verification
- Computer Vision
- Real-time Inference

---

## Objective

Build a real-time system for:

1. Attendance Liveness Verification
2. Interview Candidate Verification

Prevent:
- Printed photo attacks
- Replay video attacks
- Screen attacks
- Static image spoofing

---

## Architecture

Camera Input
→ Face Detection
→ Face Crop
→ Anti-Spoofing
→ Behavioral Verification
→ Physiological Verification
→ Fusion
→ Decision Engine
→ Dashboard

---

## Tech Stack

Frontend:
- Flutter (with Dart FFI for performance)

Backend:
- FastAPI (WebSocket-based streaming)

ML:
- PyTorch (Training)
- ONNX Runtime (Production Inference)
- OpenCV
- MediaPipe
- Ultralytics

Communication:
- WebSockets (Real-time stream)
- Protobuf/MessagePack (Efficient serialization)

Database:
- Firebase (Realtime DB + Firestore)

Deployment:
- Docker + NVIDIA Container Toolkit

---

## Models

Face Detection:
- YOLOv8-face

Anti-Spoofing:
- MiniFASNet (primary)
- EfficientNet-B0 (comparison)

Behavior:
- MediaPipe Face Mesh

Physiological:
- rPPG + 1D CNN

---

## Datasets

Anti-Spoof:
- CASIA FASD
- Replay Attack
- CelebA-Spoof
- SiW

Physiological:
- PURE
- UBFC-rPPG

Behavior:
- CEW

Custom Dataset:
- Blink
- Smile
- Head Turn
- Phone Replay
- Laptop Replay

---

## Metrics

Classification:
- Accuracy
- ROC-AUC
- Confusion Matrix

Anti-Spoof Metrics:
- APCER
- BPCER
- ACER

Runtime:
- FPS
- Inference Time

---

## Repository Structure

data/
models/
notebooks/
training/
inference/
backend/
frontend/
deployment/

---

## Rules

Prefer lightweight real-time models.

Use notebook:
right-evaluate-sfas.ipynb as anti-spoof baseline.

Keep inference real time.

Prefer PyTorch.

Target deployment latency <100 ms.

## graphify

This project has a graphify knowledge graph at graphify-out/.

Rules:
- Before answering architecture or codebase questions, read graphify-out/GRAPH_REPORT.md for god nodes and community structure
- If graphify-out/wiki/index.md exists, navigate it instead of reading raw files
- For cross-module "how does X relate to Y" questions, prefer `graphify query "<question>"`, `graphify path "<A>" "<B>"`, or `graphify explain "<concept>"` over grep — these traverse the graph's EXTRACTED + INFERRED edges instead of scanning files
- After modifying code files in this session, run `graphify update .` to keep the graph current (AST-only, no API cost)
