# SHIELD Developer Debugging Guide

This document outlines the observability tools and debugging practices available in SHIELD V2 to assist with CDAC presentations, testing, and future development.

## 1. Demo Mode
Demo Mode provides a live, visual overlay of the inference pipeline directly on the processed video frames, utilizing `cv2.imshow` locally on the server. This mode is visualization-only and does not alter the JSON responses sent back to the Flutter client.

**How to Enable:**
Set the `DEMO_MODE` environment variable before starting the backend:
```bash
DEMO_MODE=true uvicorn backend.main:app --host 0.0.0.0 --port 8000
```
**What is Displayed:**
* Real-time Processing FPS
* Pipeline Latency (ms)
* Current Verdict (Live, Spoof, Low Quality, etc.)
* YOLO Face Bounding Boxes
* MediaPipe Facial Landmarks (Mesh overlay)
* Active Challenge State & Detection Status

## 2. Inspecting Logs
The backend uses Python's `logging` module to output structured logs (INFO/WARNING/ERROR) to the console, removing all legacy `print()` statements. Additionally, the backend generates a **Session Timeline Log** for every websocket connection.

**Locating Session Logs:**
Logs are written as `.jsonl` files to: `logs/sessions/session_<UUID>.jsonl`

**Log Structure:**
Each line represents a processed frame containing:
* `timestamp`: Epoch time
* `session_id`: Unique connection UUID
* `frame_number`: The sequential frame ID from the client
* `latency_ms`: Total inference processing time for that frame
* `verdict` & `confidence`: Fusion output

## 3. Tracing Latency & Metrics
To inspect the live health and performance of the backend, two REST endpoints are available:

**Health Check:**
```
GET /health
```
Returns subsystem availability and memory usage.

**Debug Metrics:**
```
GET /metrics/debug
```
Returns JSON containing live metrics like `average_latency`, `frames_processed`, `frames_dropped`, `uptime`, and `backend_fps`.

## 4. Common Failures & Recovery

* **Latency Spikes (> 100ms):**
  * *Cause:* MediaPipe falling out of `VIDEO` tracking mode due to extreme head movement or low lighting, forcing a cold-start image detection.
  * *Recovery:* Ensure the user stays centered and well-lit. The pipeline will automatically recover tracking on the next clear frame.
* **rPPG Domain Gap False Negatives:**
  * *Cause:* Baseline drift in real-world lighting causing the synthetic-trained 1D-CNN to output 0.0 probability.
  * *Recovery:* This is a known model limitation. rPPG fusion weight is intentionally set to `0.0`.
* **SEB Trust Verification Failed (1008 Disconnect):**
  * *Cause:* Connecting from an unauthorized browser or missing SEB cryptographic headers.
  * *Recovery:* Use the authorized Safe Exam Browser, or disable SEB verification in the `.env` (development only).
