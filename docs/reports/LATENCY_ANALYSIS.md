# Latency Analysis

## Inference Latency
The ONNX model inference latency (time to forward-pass a `[1, 1, 150]` tensor) was profiled:
- **Average Inference Time**: ~0.14 milliseconds (0.00014s).
- **Time to First Prediction**: Negligible compute overhead, highly dominated by data collection.

## Total Pipeline Latency
While the ONNX inference itself takes under 1ms, the upstream SHIELD pipeline includes:
- Frame decoding
- YOLOv8 Face Detection & Segmentation
- MiniFASNet Quality Gates & Anti-Spoofing
- Facial Landmark Behavior extraction

From PR-019, the overall pipeline latency per frame is roughly **250ms (4 FPS)**.

## Challenge Timeout Constraints
To reach 150 frames, the pipeline must process 150 frames. 

**Time Required to Accumulate 150 Frames**:
`150 frames * 250ms/frame = 37.5 seconds`

**Comparison Against Timeouts**:
- **5 Second Challenge**: Processes ~20 frames. Fails to reach 150.
- **10 Second Challenge**: Processes ~40 frames. Fails to reach 150.
- **15 Second Challenge**: Processes ~60 frames. Fails to reach 150.

**Conclusion**: The latency bottleneck is entirely in the upstream pipeline (YOLO / MiniFASNet), not the rPPG ONNX model. However, because the upstream latency drags the pipeline down to 4 FPS, the system requires 37.5 seconds of sustained execution to accumulate the 150 frames needed for the rPPG ONNX model to evaluate a single window.
