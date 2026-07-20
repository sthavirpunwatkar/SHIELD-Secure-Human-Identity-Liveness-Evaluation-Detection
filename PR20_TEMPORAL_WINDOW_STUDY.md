# PR-020: Temporal Window Feasibility Study - Final Verdict

This document summarizes the findings of the temporal window sensitivity study and answers the core research objectives.

## Core Questions & Findings

**1. Is 150 frames a hard requirement of the trained model?**
Yes. The `RPPGCNNv2` ONNX graph is exported with strictly static dimensions of `[1, 1, 150]`. 

**2. Is 150 frames merely an implementation choice?**
No. It is a fundamental structural and mathematical property of the model. The `FrequencyBranch` relies on an FFT applied over exactly 150 elements, expecting a biologically valid spectrum containing at least 4-8 cardiac cycles. The network layers mathematically assume the input tensor represents a contiguous 5.0-second signal at 30 FPS.

**3. Can the model produce reliable predictions using fewer frames?**
No. Experimental evidence demonstrates that simulating shorter sequences (by applying zero-padding to reach the required 150 tensor length) instantly crashes the model's confidence to `0.0000`.

**4. If fewer frames work, why?**
N/A. They do not work.

**5. If they do not work, why not?**
The frequency domain features are highly sensitive. When a short sequence (e.g., 60 frames) is padded with 90 zeros, it introduces a severe step-function discontinuity in the time domain. This completely shatters the FFT spectrum, creating massive spectral leakage that destroys the physiological signal. The model correctly interprets this corrupted spectrum as a spoof or invalid signal, resulting in a confidence of 0.0.

**6. Is the current deployment architecture compatible with the model?**
Absolutely not.

**7. What architectural mismatch exists?**
The rPPG model inherently assumes a continuous 30 FPS biological feed. However, the production backend operates synchronously, pushing every frame through heavy spatial models (YOLOv8, MiniFASNet) before rPPG can extract the ROI. This chokes backend throughput to ~4 FPS. Because the liveness challenge strictly times out after 5.0 seconds, the backend can mathematically only process ~20 frames before the session ends. Thus, the 150-frame requirement is impossible to meet within the product's UX constraints.

**8. What is the scientifically justified recommendation?**
We recommend a two-phased approach:
*   **Immediate Mitigation (Option D - Dynamic Readiness)**: Refactor `FusionEngine` to accept a `None` or `NotReady` state instead of defaulting to `0.0`. If `len(buffer) < 150`, rPPG should safely abstain from the fusion vote, allowing the authentication challenge to succeed based on MiniFASNet and behavior metrics.
*   **Long-Term Resolution (Option B - Decoupled Streaming)**: The backend architecture must be decoupled. The rPPG extraction (a lightweight crop and average) must run in a dedicated fast-lane async thread capable of matching the frontend's 30 FPS, while the heavy spatial models evaluate frames asynchronously in a separate pool. This ensures the rPPG buffer fills within 5 seconds without stalling the pipeline.
