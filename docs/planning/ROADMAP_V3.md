# SHIELD V3 Engineering Roadmap

## Epic 1: Native Flutter Encoder Plugin
**Target:** Develop a custom Flutter plugin bridging `CameraImage` buffers to Android `MediaCodec` and iOS `VideoToolbox` for real-time H.264 Annex B encoding.
- **Complexity:** High
- **Risk:** High (Zero-copy buffer management, latency)
- **Dependencies:** None

## Epic 2: Desktop Encoding
**Target:** Implement a GStreamer or FFmpegKit fallback for Linux/Windows desktop targets to mirror mobile hardware encoding.
- **Complexity:** Medium
- **Risk:** Low (Standard C++ FFI)
- **Dependencies:** Epic 1 (Interface finalization)

## Epic 3: Real Dataset Collection
**Target:** Gather diverse attack vectors (paper, screens, 3D masks) across multiple demographics for scientific rPPG baseline validation.
- **Complexity:** Medium
- **Risk:** Medium (Data privacy, demographic balance)
- **Dependencies:** Epic 1 & 2 (Requires working streaming pipeline)

## Epic 4: rPPG Retraining
**Target:** Fine-tune the 3D CNN rPPG model on the newly collected continuous video dataset to drastically reduce False Acceptance Rates (FAR).
- **Complexity:** High
- **Risk:** Medium (Model convergence)
- **Dependencies:** Epic 3

## Epic 5: Production Monitoring
**Target:** Integrate Prometheus/Grafana metrics into the Fusion Pipeline to monitor real-time inference latency and model confidence intervals.
- **Complexity:** Low
- **Risk:** Low
- **Dependencies:** None

## Epic 6: Cloud Deployment
**Target:** Containerize the SHIELD backend into a Kubernetes-ready Helm chart with horizontal GPU scaling and zero-downtime rolling updates.
- **Complexity:** Medium
- **Risk:** Low
- **Dependencies:** None
