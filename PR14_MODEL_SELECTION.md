# PR-014: PyTorch rPPG Model Selection

## Phase 1 & 2: Baseline Identification & Selection

Our goal was to identify and integrate a PyTorch-native rPPG baseline that possesses official, easily accessible pretrained weights to overcome the framework limitations encountered with TS-CAN.

### Model Candidates Evaluated

1. **PhysNet** (Priority 1)
   - **Repository:** Multiple variants (e.g., ZitongYu original, rPPG-Toolbox, Hugging Face ports).
   - **Pretrained Weights:** We identified a PyTorch-native `.pt` state dictionary hosted by `vision-cardio-rppg` on Hugging Face (`rppg_physnet_ubfc.pt`), which perfectly matches the standard 3D CNN Spatio-Temporal Encoder-Decoder framework.
   - **Framework:** Native PyTorch.
   - **License:** MIT License / Open-Source research.

2. **EfficientPhys**
   - Typically implemented inside the broad `rPPG-Toolbox`. While highly performant, directly accessible official weights (without requiring dataset EULA sign-offs or Google Drive downloads) proved more difficult to integrate autonomously.

3. **PhysFormer**
   - Excellent Transformer-based model, but higher overhead and less straightforward pre-trained weight distribution compared to the simpler CNN architectures.

### Selection Decision
**PhysNet** was selected as it is the highest-priority model on the candidate list. A compatible PyTorch weight file was readily available and successfully downloaded. Because the architecture relies on standard `Conv3d`, `MaxPool3d`, and `BatchNorm3d` operations, it integrates into our adapter natively without any custom CUDA kernels or TensorFlow dependencies.
