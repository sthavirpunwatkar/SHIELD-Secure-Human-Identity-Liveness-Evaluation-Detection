# Architectural Options

This document evaluates strategies to resolve the architectural mismatch between the 150-frame rPPG model constraint and the 4 FPS pipeline constraint.

## Option A: Keep 150-frame requirement, Increase challenge duration
Extend the challenge duration from 5.0 seconds to 40.0+ seconds to allow the 4 FPS backend to accumulate 150 frames.
- **Advantages**: Requires zero code changes to the pipeline or model.
- **Limitations**: Severe UI/UX degradation. A 40-second liveness challenge is unacceptable for an authentication product.
- **Engineering Complexity**: Minimal (one variable change).
- **Scientific Validity**: Technically valid, but breaks the 5.0s biological liveness premise.
- **Deployment Impact**: User dropout rate will spike; highly unfeasible.

## Option B: Streaming temporal inference
Run the heavy YOLO/MiniFASNet models selectively (e.g., once every 10 frames) while letting the rPPG ROI extraction run on every frame.
- **Advantages**: Keeps the backend FPS closer to 30 FPS, allowing 150 frames to be processed within 5 seconds.
- **Limitations**: Security risk. An attacker might swap a mask in during the 9 frames that Anti-Spoofing is skipped. 
- **Engineering Complexity**: High. Requires rewriting `fusion_service.py` to support asynchronous/branching pipelines.
- **Scientific Validity**: Moderate. 
- **Deployment Impact**: Requires massive backend refactoring.

## Option C: Sliding-window inference
Run the frontend capture at a lower FPS (e.g., 5 FPS) and use a sliding window over 150 frames.
- **Advantages**: Less load.
- **Limitations**: At 5 FPS, it takes 30 seconds to gather 150 frames. The rPPG biology fundamentally requires continuous 30 FPS sampling to capture high-frequency cardiac signals without aliasing (Nyquist theorem).
- **Engineering Complexity**: Low.
- **Scientific Validity**: Invalid. 5 FPS violates the Nyquist rate for capturing a 1-2 Hz cardiac signal cleanly.
- **Deployment Impact**: Ruins model accuracy.

## Option D: Dynamic readiness state
Modify `FusionEngine` to accept `None` or `NotReady` from the rPPG model instead of `0.0`. If rPPG is not ready when the challenge expires, the fusion engine falls back to weighing just YOLO/MiniFASNet/Blink.
- **Advantages**: Immediate fix for the `0.0000` confidence bug. Allows the system to function securely using other modalities.
- **Limitations**: The rPPG model will *never* be utilized in production if the challenge is 5.0s, rendering it dead code.
- **Engineering Complexity**: Low.
- **Scientific Validity**: Valid systems-level handling of missing data.
- **Deployment Impact**: High safety, but acknowledges the rPPG feature is dead.

## Option E: Model redesign requiring retraining
Retrain a new `RPPGCNNv3` model capable of operating on variable sequence lengths (e.g., using an RNN/LSTM or Transformer instead of fixed CNN+FFT) or operating on fewer frames (e.g., 60 frames = 2 seconds).
- **Advantages**: Mathematically and structurally fixes the mismatch.
- **Limitations**: Extremely expensive. Requires a full data science life cycle.
- **Engineering Complexity**: Very High.
- **Scientific Validity**: The most robust long-term solution.
- **Deployment Impact**: Blocked by retraining time.
