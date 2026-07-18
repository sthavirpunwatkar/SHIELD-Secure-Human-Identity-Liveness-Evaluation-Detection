# PR-010C SIW BASELINE BENCHMARK

## 1. Model Compatibility Check (STEP 0)
The production Anti-Spoof model (`models/efficientnet_fas.onnx`) exposes the following inference requirements based on `inference/antispoof/inference.py`:
* **ONNX Input Shape:** `(1, 3, 224, 224)` (for efficientnet variant)
* **ONNX Input Dtype:** `float32`
* **Input Resolution:** Fixed `224x224`
* **RGB vs BGR:** BGR (OpenCV default expected)
* **Resize Method:** Bilinear interpolation (`cv2.resize`)
* **Crop Strategy:** Tight face bounding box required prior to inference.
* **Pixel Normalization:** Min-Max scaling (`/ 255.0`)
* **Mean/std Normalization:** None explicitly applied.

**Compatibility Verdict:** SiW provides raw, uncropped full-frame video (usually `.mov` or `.mp4`). The benchmark harness will need to apply a face detector (e.g., the production `YoloDetector`) to generate the required tight face crops before routing the tensor to `AntiSpoofRunner`. **No inference or preprocessing changes are required**; the framework simply must simulate the frontend's bounding box crop logic.

## 2. Dataset Preparation (STEP 1)
* **Official Source:** Michigan State University (CVLab) / IEEE
* **Access Requirements:** Requires signing an End User License Agreement (EULA) and formal request to the authors.
* **License:** Academic, non-commercial use only.
* **Protocol Version:** Protocol 1, 2, and 3.
* **Attack Categories:** Printed Photo, Tablet Replay, Mobile Replay, Silicone Mask.
* **Subject Count:** 165 individuals.
* **Expected Directory Structure:**
  ```text
  benchmark/datasets/SiW/
    ├── Protocol_1/
    │     ├── train/
    │     └── test/
    ├── Protocol_2/
    └── Protocol_3/
  ```

## 3. Harness Validation (STEP 2)
The `AntiSpoofRunner` perfectly wraps the production module.
* **Model Checksum:** Validated matching SHA256 against production.
* **Absolute Path:** `models/efficientnet_fas.onnx`
* **Provider:** CPUExecutionProvider / CUDAExecutionProvider
* **Tensor Shape:** `(1, 3, 224, 224)`
* **Tensor Dtype:** `float32`

## 4. Benchmark Execution Status (STEP 3 - 7)
**[STOP CONDITION TRIGGERED]**

The SiW dataset is currently missing from the local filesystem (`benchmark/datasets/SiW/`). To maintain absolute scientific integrity, **no benchmark results, metrics, or graphs have been fabricated.**

The `benchmark/utils/dataset_validator.py` parser successfully verified the configuration and triggered the safety halt. 

### Required Action
Please mount or download the official SiW dataset adhering to the structure outlined in Section 2. Once the files are present, the `evaluate_siw.py` script will automatically unblock and execute the metrics, error analysis, and visualization sweeps.

## Conclusion
The current Anti-Spoof benchmark is blocked pending dataset availability. No conclusions regarding model performance can be drawn without measured evidence.
