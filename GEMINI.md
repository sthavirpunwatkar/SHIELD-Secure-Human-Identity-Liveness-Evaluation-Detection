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

This project has a knowledge graph at graphify-out/ with god nodes, community structure, and cross-file relationships.

Rules:
- For codebase questions, first run `graphify query "<question>"` when graphify-out/graph.json exists. Use `graphify path "<A>" "<B>"` for relationships and `graphify explain "<concept>"` for focused concepts. These return a scoped subgraph, usually much smaller than GRAPH_REPORT.md or raw grep output.
- If graphify-out/wiki/index.md exists, use it for broad navigation instead of raw source browsing.
- Read graphify-out/GRAPH_REPORT.md only for broad architecture review or when query/path/explain do not surface enough context.
- After modifying code, run `graphify update .` to keep the graph current (AST-only, no API cost).

## Workflow Hooks

After completing each major goal or task, the following actions MUST be performed:
1. **Update Graph:** Run `graphify update .` to synchronize the knowledge graph with the latest code changes.
2. **Update Documentation:** Ensure `PROJECT_DIARY.md` and `README.md` reflect the latest progress.
3. **Synchronize:** Push all committed changes to the remote repository (`git push origin main`).
4. **Audit:** After each feature creation or goal completion, invoke the `overview_agent` to perform a senior-level audit and fix any inconsistencies.
