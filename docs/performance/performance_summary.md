# SHIELD Pipeline Performance Summary

## Inference Latency Breakdown
The following metrics represent the average per-frame processing latency during a continuous active challenge session (30 FPS input stream).

| Subsystem | Model / Algorithm | Avg Latency (ms) | Peak Latency (ms) |
| --- | --- | --- | --- |
| **Face Detection & ROI** | YOLOv8-seg (Nano) | 6.3 ms | 8.5 ms |
| **Behavioral Analysis** | MediaPipe (VIDEO Mode) | 3.2 ms | 5.1 ms |
| **Anti-Spoofing** | MiniFASNet (ONNX int8) | ~0.61 ms | 1.2 ms |
| **rPPG** | 1D-CNN (ONNX int8) | ~0.45 ms | 0.8 ms |
| **Fusion Logic** | Rule Engine | < 0.1 ms | < 0.1 ms |
| **Total Pipeline (Backend)** | End-to-End | **~10.66 ms** | **~15.7 ms** |

## Throughput & System Metrics
* **Backend Processing Capacity:** The async pipeline can sustain up to ~93 FPS on a single core before queue saturation.
* **Target Stream Rate:** Locked at 30 FPS.
* **Memory Footprint:** ~120 MB RSS per active Python worker (Models loaded in memory).
* **CPU Utilization:** ~10% - 15% per active session on standard hardware.
* **Streaming Bandwidth:** ~1.5 Mbps - 2.5 Mbps per client depending on H.264 compression bitrate and frame complexity.

## Optimization Notes
1. **MediaPipe `VIDEO` mode** allows for temporal tracking, heavily optimizing consecutive frame landmark extraction.
2. **YOLO JPEG Compression Defense** runs extremely fast natively via OpenCV encoding buffer without significant overhead.
3. Both ONNX engines (MiniFASNet and rPPG) utilize Int8 quantization, executing in under 1ms on the CPU.
