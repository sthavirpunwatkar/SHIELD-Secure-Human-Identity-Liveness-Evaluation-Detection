# Release Notes - SHIELD V2 RC1

## Highlights
SHIELD V2 RC1 marks a major milestone in transitioning from a batch-oriented inference pipeline to a fully asynchronous, real-time streaming architecture. This Release Candidate focuses on extreme optimization, low-latency execution, and event-driven architecture designed for high-throughput continuous liveness evaluation.

## Completed PRs
* **PR-001 (Continuous Streaming Architecture):** Replaced legacy HTTP REST endpoints with asynchronous WebSockets, enabling real-time bidirectional frame streams and reducing end-to-end transport overhead.
* **PR-002 (Frame Transport Abstraction):** Standardized frame decoding, implementing efficient circular buffering and thread-safe pipeline distribution for YOLO, MediaPipe, and rPPG tasks.
* **PR-003 (MediaPipe VIDEO Mode Integration):** Upgraded facial landmark tracking from static `IMAGE` mode to temporal `VIDEO` mode, drastically reducing jitter and improving tracking stability across sequential frames.
* **PR-004 (Event-Driven Backend & Fusion):** Migrated the backend to a fully event-driven state machine encompassing the `ChallengeEngine` and `FusionService`, streamlining behavioral challenge tracking and response evaluation.
* **PR-005 (rPPG Reintegration & Scientific Validation):** Re-integrated the rPPG ONNX engine into the continuous stream. Conducted empirical optimization identifying the right cheek as the superior ROI (SNR: 6.62 dB). Validated pipeline stability over extensive 10-minute 30fps benchmarks (Latency ~0.61ms, Zero Memory Leaks).
* **PR-005.5 (Root Cause Validation for rPPG V2):** Executed a highly isolated scientific investigation to trace remaining confidence anomalies in the rPPG output. Determined definitively via KL Divergence and PyTorch forward hooks that the root cause is a measurable synthetic-to-real domain gap stemming from heavy reliance on synthetic training data.

## Known Issues
* The rPPG subsystem produces false negatives (`0.0` probability) on real-world inputs due to the synthetic-to-real domain gap. The model is currently disabled in the `FusionService` (weight set to `0.0`) to preserve overall system reliability.
* Automated Flutter CI tests are currently skipped due to missing SDK dependencies in the validation environment.

## Future Work
* Collect and curate a comprehensive dataset of real human rPPG signals (incorporating natural lighting and motion drift).
* Retrain the rPPG 1D-CNN pipeline utilizing the new dataset.
* Implement Active Defenses and future architectural designs specified in the ADRs.
