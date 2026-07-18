# PR-011: Adapter Specification

## Objective
Design isolation adapters for the selected external benchmark models (MiniFASNet and TS-CAN) such that they can operate within the SHIELD benchmarking harness *without* modifying SHIELD production code, inference pipelines, or thresholds.

## Architectural Guidelines
1. **Strict Isolation:** The adapter must implement a standard benchmark harness interface (e.g., `IBenchmarkModel`).
2. **Read-Only Context:** The adapter receives a copy of the SHIELD context (or raw frames) and cannot mutate them.
3. **Black-box Mapping:** The adapter is solely responsible for transforming SHIELD's unified tensor formats into the specific inputs expected by the external models, and mapping their raw outputs back into the benchmark's evaluation schema.

---

## 1. Anti-Spoofing Adapter (MiniFASNet)

### Input Transformation
*   **Intercept SHIELD Input:** Receives the standard SHIELD bounding box and raw frame.
*   **Scale:** Expand the bounding box using the model's required 2.7x scale factor.
*   **Crop & Resize:** Crop the expanded face area and use bilinear interpolation to resize to exactly `80x80` pixels.
*   **Color Conversion:** Ensure the image is converted to `BGR` format if SHIELD provides `RGB`.
*   **Normalization:** Convert from `[0, 255]` integers to `[0.0, 1.0]` floats. Reshape to `(1, 3, 80, 80)`.

### Execution
*   Invoke the MiniFASNet ONNX runtime (or PyTorch `forward` pass) strictly in inference mode (`torch.no_grad()`).

### Output Transformation
*   **Intercept Output:** The model outputs a raw logits tensor of shape `(1, 2)` or `(1, 3)`.
*   **Softmax:** Apply softmax to extract the liveness probability.
*   **Mapping:** Return a standardized `BenchmarkResult(liveness_score=probability, classification="REAL" | "SPOOF")` object to the benchmark harness.

---

## 2. rPPG Adapter (TS-CAN)

### Input Transformation
*   **Buffer Management:** SHIELD processes frames continuously. The adapter must instantiate a rolling buffer (e.g., of size `T=10` or whatever the TS-CAN checkpoint requires).
*   **Extraction:** For each incoming frame, extract the face crop.
*   **Resize:** Resize the face crop to `36x36` pixels.
*   **Normalization & Differencing:** Apply temporal differencing across the buffered frames as required by TS-CAN's motion branch. Normalize the appearance frame (typically the first or middle frame of the buffer).
*   **Tensor Layout:** Formulate the input tensor sequence `(B, T, C, H, W)`.

### Execution
*   Trigger inference only when the temporal buffer is full.
*   Execute TS-CAN isolated forward pass.

### Output Transformation
*   **Intercept Output:** The model outputs a continuous 1D array representing the pulse waveform.
*   **Mapping:** Return a `BenchmarkTimeSeriesResult(waveform=output_array, bpm=calculated_hr)` object to the benchmark harness for comparison against SHIELD's proprietary rPPG pipeline.
