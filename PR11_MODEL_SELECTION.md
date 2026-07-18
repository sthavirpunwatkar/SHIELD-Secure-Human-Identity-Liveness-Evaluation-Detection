# PR-011: External Pretrained Model Selection

## Phase 1: Model Research

### Anti-Spoofing Models

#### 1. Silent-Face-Anti-Spoofing (MiniFASNet)
*   **Official Paper:** "Silent-Face-Anti-Spoofing" (Open-source release by Minivision)
*   **Official GitHub:** [minivision-ai/Silent-Face-Anti-Spoofing](https://github.com/minivision-ai/Silent-Face-Anti-Spoofing)
*   **Official Pretrained Weights:** Available in the repo (`.pth` files such as `2.7_80x80_MiniFASNetV2.pth`).
*   **License:** MIT License
*   **Framework:** PyTorch
*   **Input Resolution:** 80x80 pixels
*   **Input Tensor Format:** `(1, 3, 80, 80)`, BGR format.
*   **Preprocessing:** Face detection, scale bounding box by 2.7x, crop, resize to 80x80, normalize pixel values to [0, 1].
*   **Output Interpretation:** Softmax probabilities (spoof vs. real score).
*   **Required Dependencies:** PyTorch, OpenCV, NumPy.
*   **Expected Latency:** Very low (lightweight edge-friendly network).
*   **ONNX Available:** Yes, conversion scripts are widely available in the community.

#### 2. CDCN (Central Difference Convolutional Networks)
*   **Official Paper:** "Searching Central Difference Convolutional Networks for Face Anti-Spoofing" (CVPR 2020)
*   **Official GitHub:** [ZitongYu/CDCN](https://github.com/ZitongYu/CDCN)
*   **Official Pretrained Weights:** Available (provided via OneDrive/Baidu links in the repo).
*   **License:** Apache 2.0 / Academic Use
*   **Framework:** PyTorch
*   **Input Resolution:** Typically 256x256
*   **Input Tensor Format:** `(1, 3, 256, 256)`, RGB.
*   **Preprocessing:** Face detection, alignment, crop, resize, standard normalization.
*   **Output Interpretation:** Depth map regression (spoof score derived from map statistics).
*   **Required Dependencies:** PyTorch, torchvision.
*   **Expected Latency:** Moderate. Frame-level processing but uses custom CDC convolutions.
*   **ONNX Available:** Possible, but custom CDC operations may require custom ONNX ops or plugins.

#### 3. DeepPixBiS
*   **Official Paper:** "Deep Pixel-wise Binary Supervision for Face Anti-Spoofing"
*   **Official GitHub:** [Saiyam26/Face-Anti-Spoofing-using-DeePixBiS](https://github.com/Saiyam26/Face-Anti-Spoofing-using-DeePixBiS)
*   **Official Pretrained Weights:** Available (`DeePixBiS.pth`).
*   **License:** MIT License
*   **Framework:** PyTorch
*   **Input Resolution:** 224x224
*   **Input Tensor Format:** `(1, 3, 224, 224)`, RGB.
*   **Preprocessing:** Face crop, resize to 224x224, ImageNet normalization.
*   **Output Interpretation:** Pixel-wise binary map and scalar spoof score (mean of the map).
*   **Required Dependencies:** PyTorch, torchvision.
*   **Expected Latency:** Higher latency due to the heavy DenseNet-161 backbone.
*   **ONNX Available:** Yes, standard operations export easily to ONNX.

### rPPG Models

#### 1. TS-CAN
*   **Official Paper:** "TS-CAN: Temporal Shift Convolutional Attention Network" (NeurIPS 2020)
*   **Official GitHub:** [xin71/MTTS-CAN](https://github.com/xin71/MTTS-CAN) & [rPPG-Toolbox](https://github.com/ubicomplab/rPPG-Toolbox)
*   **Official Pretrained Weights:** Available via the official repo and rPPG-Toolbox.
*   **License:** MIT License
*   **Framework:** TensorFlow (Original) / PyTorch (rPPG-Toolbox)
*   **Input Resolution:** 36x36
*   **Input Tensor Format:** Video sequence `(B, T, C, H, W)` or `(T, C, 36, 36)`.
*   **Preprocessing:** Face detection, crop, resize, spatial-temporal normalization, and frame differencing.
*   **Output Interpretation:** Continuous 1D physiological pulse waveform.
*   **Required Dependencies:** PyTorch, SciPy.
*   **Expected Latency:** ~12 ms/frame (highly optimized, real-time capable).
*   **ONNX Available:** Yes.

#### 2. PhysNet
*   **Official Paper:** "Remote Photoplethysmograph Signal Measurement from Facial Videos Using Spatio-Temporal Networks" (BMVC 2019)
*   **Official GitHub:** [ZitongYu/PhysNet](https://github.com/ZitongYu/PhysNet) & [rPPG-Toolbox](https://github.com/ubicomplab/rPPG-Toolbox)
*   **Official Pretrained Weights:** Available via community links and toolboxes.
*   **License:** MIT License
*   **Framework:** PyTorch
*   **Input Resolution:** 32x32 or 128x128
*   **Input Tensor Format:** 3D spatio-temporal tensor `(C, T, H, W)`.
*   **Preprocessing:** Face tracking, crop, resize, sequence batching.
*   **Output Interpretation:** 1D pulse waveform.
*   **Required Dependencies:** PyTorch, OpenCV.
*   **Expected Latency:** High (heavy 3D CNN).
*   **ONNX Available:** Yes, but 3D convolutions can be slower in some ONNX runtimes.

#### 3. RhythmMamba
*   **Official Paper:** "RhythmMamba: Fast Remote Physiological Measurement with State Space Models" (2024)
*   **Official GitHub:** [zizheng-guo/RhythmMamba](https://github.com/zizheng-guo/RhythmMamba)
*   **Official Pretrained Weights:** Available in the repo.
*   **License:** MIT License
*   **Framework:** PyTorch
*   **Input Resolution:** Configurable (e.g., 128x128)
*   **Input Tensor Format:** Sequence tensor `(B, T, C, H, W)`.
*   **Preprocessing:** Face crop, resize, temporal batching.
*   **Output Interpretation:** 1D pulse waveform.
*   **Required Dependencies:** PyTorch, `causal-conv1d`, `mamba-ssm`.
*   **Expected Latency:** Low latency, high throughput.
*   **ONNX Available:** No/Poor. Mamba state-space models currently lack robust ONNX export support.

---

## Phase 2: Model Ranking

### Anti-Spoofing Ranking
1. **Silent-Face-Anti-Spoofing (MiniFASNet):** **Rank 1**. Extremely low latency, high production suitability, minimal dependencies, flawless ONNX support.
2. **DeepPixBiS:** **Rank 2**. Excellent reproducibility, but the DenseNet-161 backbone introduces unnecessary latency.
3. **CDCN:** **Rank 3**. Great academic baseline, but custom CDC convolutions make ONNX export and maintenance riskier.

### rPPG Ranking
1. **TS-CAN:** **Rank 1**. Perfect balance of inference speed (~12ms/frame) and reproducibility via rPPG-Toolbox. Easy integration.
2. **RhythmMamba:** **Rank 2**. Unmatched theoretical speed/memory, but custom Mamba CUDA kernels severely hurt maintainability and ONNX export.
3. **PhysNet:** **Rank 3**. Solid 3D-CNN baseline but computationally heavy and slow.

---

## Phase 3: Selection

### Selected Anti-Spoofing Model: Silent-Face-Anti-Spoofing (MiniFASNet)
**Rationale:** The SHIELD framework demands high inference speed and robust reproducibility. MiniFASNet's small footprint (80x80 input) and minimal dependencies make it the undisputed choice. It natively exports to ONNX and eliminates the need for custom CUDA kernels.

### Selected rPPG Model: TS-CAN
**Rationale:** TS-CAN offers real-time inference (averaging 12ms per frame) by using an efficient temporal shift module rather than expensive 3D convolutions. It is fully integrated into the standard rPPG-Toolbox, providing a clear path for integration into our benchmark harness without modifying our production logic.
