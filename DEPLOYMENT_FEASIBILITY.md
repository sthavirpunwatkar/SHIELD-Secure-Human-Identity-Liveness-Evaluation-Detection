# Deployment Feasibility

## Current Operational Metrics
- **Frontend FPS**: ~30 FPS (Frames dispatched via WebCodecs & WebSockets)
- **Backend FPS**: ~4 FPS (Constrained by YOLO segmentation & Anti-Spoofing heavy pipeline)
- **Maximum Achievable Throughput**: ~4 FPS. (Even with perfect networking, CPU-bound inference bottlenecks the stream).
- **Challenge Timeout**: 5.0 Seconds.

## Capacity Constraints
- **Frames Available Before Timeout**: `4 FPS * 5 seconds = 20 frames`.
- **Expected Buffer Fill Time (150 frames)**: `150 frames / 4 FPS = 37.5 seconds`.

## Deployment Analysis
There is a fundamental architectural mismatch between the trained `RPPGCNNv2` model and the SHIELD deployment environment:
1. The model was trained specifically on 30 FPS data with exactly 150-frame windows (5 seconds).
2. The deployed backend operates synchronously per frame, resulting in an effective processing rate of 4 FPS.
3. Because the backend evaluates frames at 4 FPS, the frontend's 30 FPS stream gets choked, heavily buffering in memory. 
4. When the 5-second challenge timer expires, the backend has only pulled ~20 frames out of the buffer, utterly failing to meet the model's strict 150-frame requirement.

**Conclusion**: The current `RPPGCNNv2` model is **structurally incompatible** with the current backend processing architecture. It is impossible to achieve a 150-frame buffer within a 5.0s window when the pipeline operates at 4 FPS.
