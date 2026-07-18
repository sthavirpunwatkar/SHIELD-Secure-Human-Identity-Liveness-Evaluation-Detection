# SHIELD PR-010D: State-of-the-Art Baseline Survey

## PART 1 — ANTI-SPOOF SURVEY

### 1. Silent-Face-Anti-Spoof (MiniFASNet)
- **Paper**: Silent Face Anti-Spoofing (minifasnet)
- **GitHub**: https://github.com/minivision-ai/Silent-Face-Anti-Spoofing
- **License**: MIT
- **Pretrained Weights**: Yes (PyTorch, ONNX, NCNN)
- **Framework**: PyTorch / NCNN
- **Input Resolution**: 80x80 (face crop)
- **Preprocessing**: Face detection, bounding box expansion, resize.
- **Datasets**: CASIA-SURF (implied/custom dataset)
- **Evaluation Metrics**: ACER, TPR@FPR
- **Inference Speed**: ~2ms on CPU (C++)
- **Maintenance Status**: Abandoned/Stale (last updated ~2020)

### 2. CDCN (Central Difference Convolutional Networks)
- **Paper**: Searching Central Difference Convolutional Networks for Face Anti-Spoofing (CVPR 2020)
- **GitHub**: https://github.com/ZitongYu/CDCN
- **License**: Apache 2.0
- **Pretrained Weights**: Yes
- **Framework**: PyTorch
- **Input Resolution**: 256x256
- **Preprocessing**: MTCNN face cropping, resize, normalization.
- **Datasets**: OULU-NPU, CASIA-MFSD, Replay-Attack
- **Evaluation Metrics**: ACER, HTER, EER
- **Inference Speed**: ~30ms on GPU
- **Maintenance Status**: Stale

### 3. CDCN++
- **Paper**: Searching Central Difference Convolutional Networks for Face Anti-Spoofing
- **GitHub**: https://github.com/ZitongYu/CDCN
- **License**: Apache 2.0
- **Pretrained Weights**: Yes
- **Framework**: PyTorch
- **Input Resolution**: 256x256
- **Preprocessing**: MTCNN face cropping
- **Datasets**: OULU-NPU
- **Evaluation Metrics**: ACER, HTER, EER
- **Inference Speed**: ~35ms on GPU
- **Maintenance Status**: Stale

### 4. DeepPixBiS (Deep Pixel-wise Binary Supervision)
- **Paper**: Deep Pixel-wise Binary Supervision for Face Anti-Spoofing (Biometrics 2019)
- **GitHub**: https://github.com/lucasb-eyer/DeepPixBiS (various implementations)
- **License**: MIT (mostly unofficial)
- **Pretrained Weights**: Yes (third-party)
- **Framework**: PyTorch
- **Input Resolution**: 224x224
- **Preprocessing**: Face crop, resize
- **Datasets**: OULU-NPU
- **Evaluation Metrics**: ACER, BPCER, APCER
- **Inference Speed**: ~15ms on GPU
- **Maintenance Status**: Stale

### 5. AENet (Auto-Expert Network)
- **Paper**: Face Anti-Spoofing via Auto-Expert Network (2020)
- **GitHub**: Code often private or integrated in larger repos
- **License**: Non-commercial / Academic
- **Pretrained Weights**: Limited/Unofficial
- **Framework**: PyTorch
- **Input Resolution**: 256x256
- **Preprocessing**: Face bounding box
- **Datasets**: OULU-NPU, SiW
- **Evaluation Metrics**: ACER
- **Inference Speed**: ~40ms on GPU
- **Maintenance Status**: Inactive

### 6. SSR-FCN (Spatial-Spectral Representation)
- **Paper**: Spatial-Spectral Representation for Face Anti-Spoofing
- **GitHub**: Varies (mostly academic)
- **License**: Academic
- **Pretrained Weights**: Rare
- **Framework**: PyTorch
- **Input Resolution**: 112x112
- **Preprocessing**: Multi-modal alignment (if applicable)
- **Datasets**: CASIA-SURF
- **Evaluation Metrics**: ACER, TPR, FPR
- **Inference Speed**: Moderate
- **Maintenance Status**: Inactive

### 7. NAS-FAS (Neural Architecture Search)
- **Paper**: Neural Architecture Search for Face Anti-Spoofing
- **GitHub**: Tied to CDCN repo usually
- **License**: Apache 2.0
- **Pretrained Weights**: Yes
- **Framework**: PyTorch
- **Input Resolution**: 256x256
- **Preprocessing**: MTCNN face crop
- **Datasets**: OULU-NPU
- **Evaluation Metrics**: ACER
- **Inference Speed**: Variable (based on searched architecture)
- **Maintenance Status**: Stale

### 8. Meta-FAS
- **Paper**: Face Anti-Spoofing with Meta-Learning (CVPR)
- **GitHub**: Varies, several implementations
- **License**: Academic
- **Pretrained Weights**: Yes (academic)
- **Framework**: PyTorch
- **Input Resolution**: 256x256
- **Preprocessing**: Domain-specific face cropping
- **Datasets**: OULU-NPU, CASIA-MFSD, Idiap, MSU
- **Evaluation Metrics**: HTER, AUC (Cross-dataset)
- **Inference Speed**: ~20ms on GPU
- **Maintenance Status**: Maintained mostly by community

## PART 2 — rPPG SURVEY

### 1. DeepPhys
- **Paper**: DeepPhys: Video-Based Physiological Measurement Using Convolutional Attention Networks (ECCV 2018)
- **GitHub**: Integrated in `rPPG-Toolbox`
- **License**: MIT (via Toolbox)
- **Pretrained Weights**: Yes
- **Framework**: PyTorch
- **Input Resolution**: 72x72
- **Preprocessing**: Motion and appearance representation derivation (normalized frame diffs).
- **Datasets**: AFRL, UBFC-rPPG
- **Evaluation Metrics**: MAE, RMSE, Pearson Correlation (r)
- **Inference Speed**: High FPS
- **Maintenance Status**: Active (via Toolbox)

### 2. PhysNet
- **Paper**: Remote Photoplethysmograph Signal Measurement from Facial Videos Using Spatio-Temporal Networks (BMVC 2019)
- **GitHub**: Integrated in `rPPG-Toolbox`
- **License**: MIT
- **Pretrained Weights**: Yes
- **Framework**: PyTorch
- **Input Resolution**: 128x128 (T=64 frames)
- **Preprocessing**: Temporal face cropping and resizing.
- **Datasets**: VIPL-HR, Oulu-Bio
- **Evaluation Metrics**: HR MAE, RMSE, SNR
- **Inference Speed**: Moderate
- **Maintenance Status**: Active (via Toolbox)

### 3. EfficientPhys
- **Paper**: EfficientPhys: Enabling Simple, Fast and Accurate Camera-Based Vitals Measurement (WACV 2023)
- **GitHub**: Integrated in `rPPG-Toolbox`
- **License**: MIT
- **Pretrained Weights**: Yes
- **Framework**: PyTorch
- **Input Resolution**: 72x72
- **Preprocessing**: Spatial-temporal cropping
- **Datasets**: UBFC-rPPG, PURE
- **Evaluation Metrics**: MAE, RMSE
- **Inference Speed**: Very Fast (Mobile-friendly)
- **Maintenance Status**: Active

### 4. PhysFormer
- **Paper**: PhysFormer: Facial Video-based Physiological Measurement with ViT (CVPR 2022)
- **GitHub**: https://github.com/ZitongYu/PhysFormer
- **License**: Apache 2.0
- **Pretrained Weights**: Yes
- **Framework**: PyTorch
- **Input Resolution**: 128x128 (T=160)
- **Preprocessing**: Face tracking, cropping, frame chunking.
- **Datasets**: VIPL-HR, PURE, UBFC-rPPG
- **Evaluation Metrics**: HR MAE, RMSE, r, SD
- **Inference Speed**: Slow (~15-20 FPS on GPU)
- **Maintenance Status**: Stale

### 5. TS-CAN (Temporal Shift Convolutional Attention Network)
- **Paper**: TS-CAN (NeurIPS 2020)
- **GitHub**: https://github.com/xliu0/ts-can (and rPPG-Toolbox)
- **License**: MIT
- **Pretrained Weights**: Yes
- **Framework**: PyTorch / TensorFlow
- **Input Resolution**: 72x72 or 36x36
- **Preprocessing**: Frame difference and appearance frames.
- **Datasets**: AFRL
- **Evaluation Metrics**: MAE, RMSE
- **Inference Speed**: High FPS
- **Maintenance Status**: Active (via Toolbox)

### 6. RhythmMamba
- **Paper**: RhythmMamba: Fast Remote Physiological Measurement with State Space Models (AAAI 2025)
- **GitHub**: https://github.com/zizheng-guo/RhythmMamba
- **License**: MIT (implied via Open-rppg)
- **Pretrained Weights**: Yes
- **Framework**: PyTorch
- **Input Resolution**: 128x128 (Variable T)
- **Preprocessing**: Frame stem (video as time series), normalization.
- **Datasets**: PURE, UBFC-rPPG
- **Evaluation Metrics**: MAE, RMSE, Pearson r
- **Inference Speed**: Very high (linear complexity)
- **Maintenance Status**: Active

### 7. PhysMamba
- **Paper**: PhysMamba: Efficient Remote Physiological Measurement with SlowFast Temporal Difference Mamba
- **GitHub**: https://github.com/JasonYpro/PhysMamba
- **License**: Apache 2.0
- **Pretrained Weights**: Yes
- **Framework**: PyTorch
- **Input Resolution**: 128x128 (Variable T)
- **Preprocessing**: Dual-stream spatial-temporal crop
- **Datasets**: PURE, VIPL-HR
- **Evaluation Metrics**: MAE, RMSE
- **Inference Speed**: High
- **Maintenance Status**: Active

### 8. PhysFormer++
- **Paper**: PhysFormer++: Facial Video-based Physiological Measurement with SlowFast Historical ViT (TPAMI)
- **GitHub**: https://github.com/ZitongYu/PhysFormer
- **License**: Apache 2.0
- **Pretrained Weights**: Yes
- **Framework**: PyTorch
- **Input Resolution**: 128x128
- **Preprocessing**: Face tracking and cropping
- **Datasets**: VIPL-HR, PURE, UBFC
- **Evaluation Metrics**: HR MAE, RMSE
- **Inference Speed**: Slow
- **Maintenance Status**: Stale

---

## PART 3 — COMPATIBILITY

**Question:** Can these models be benchmarked WITHOUT modifying SHIELD?

**Answer:** **NO.**

**Explanation exactly why:**
The SHIELD pipeline is frozen. A pretrained model cannot be plugged into SHIELD's benchmark harness "as-is" because every model possesses differing fundamental assumptions:
1. **Different Input Size:** SHIELD has a fixed tensor size assumption. MiniFASNet requires 80x80, CDCN requires 256x256, DeepPhys requires 72x72, and PhysFormer requires 128x128.
2. **Different Preprocessing:** SHIELD performs a specific cropping and normalization routine. DeepPhys requires normalized frame differences (motion and appearance streams), TS-CAN requires temporal shifts, and PhysFormer requires strict spatiotemporal face tracking chunks.
3. **Different Temporal Window:** rPPG models have varying frame requirements. PhysNet assumes T=64, PhysFormer assumes T=160, and RhythmMamba assumes arbitrary T but needs sequential state passage. SHIELD's temporal window will clash.
4. **Different Tensor Layout:** Models expect specific channel orderings (e.g., TCHW vs CTHW) and color spaces (RGB vs YUV or normalized differences).
5. **Different ROI Assumptions:** Some models expect the background to be masked, others need a loose bounding box, and others (like MiniFASNet) expect a strict, scaled coordinate expansion.
6. **Different Framework:** While most are PyTorch, passing SHIELD's in-memory data structures directly to a third-party model requires an adapter or wrapper script; native evaluation is impossible without code shims.
