# SHIELD PR-010E: Dataset Execution Order

## Part 1: Face Anti-Spoof (FAS) Execution Sequence

### 1. SiW v2 (Spoof in the Wild)
- **Protocol**: Cross-attack / cross-medium generalization protocols.
- **Attack types**: Print, Replay, 3D mask, paper glasses, transparent masks.
- **Labels**: Binary (Live / Spoof) with fine-grained attack type metadata.
- **Evaluation metric**: ACER (Average Classification Error Rate), TPR@FPR=1%, EER.
- **Expected harness adapter**: Face detection bounding box crop with specific padding, normalized to model input size.

### 2. CASIA-FASD
- **Protocol**: Standard intra-dataset testing protocols.
- **Attack types**: Warped photo, cut photo, video replay.
- **Labels**: Live / Spoof.
- **Evaluation metric**: HTER (Half Total Error Rate), EER.
- **Expected harness adapter**: Strict frame cropping and color space normalization.

### 3. Replay-Attack
- **Protocol**: Fixed split (train/devel/test).
- **Attack types**: Print, digital photo, video (mobile, high-res screen).
- **Labels**: Live / Spoof.
- **Evaluation metric**: HTER.
- **Expected harness adapter**: Frame resizing, potential illumination correction adapter.

### 4. OULU-NPU
- **Protocol**: Protocols 1-4 (evaluating illumination, capture device, cross-device, and cross-attack generalization).
- **Attack types**: Print (two printers), video replay (two displays).
- **Labels**: Live / Spoof.
- **Evaluation metric**: ACER, BPCER, APCER.
- **Expected harness adapter**: Sequence-based frame extraction, strict normalization matching original OULU baseline parameters.

---

## Part 2: rPPG Execution Sequence

### 1. UBFC-rPPG
- **Frame rate**: Uncompressed ~30 fps.
- **Labels**: Continuous PPG waveform.
- **Heart-rate annotations**: Ground truth heart rate (BPM) derived from CMS50E pulse oximeter.
- **Evaluation metrics**: MAE (Mean Absolute Error), RMSE (Root Mean Square Error), Pearson r (Correlation).
- **Preprocessing assumptions**: Subject stationary, face strictly aligned, temporal windowing (e.g., T=64, 128) applied.

### 2. PURE (Pulse Rate Extraction Dataset)
- **Frame rate**: ~30 fps (lossless PNG sequence).
- **Labels**: Continuous PPG waveform.
- **Heart-rate annotations**: Ground truth from pulse oximeter, encompassing different head motions (steady, talking, slow/fast translation, rotation).
- **Evaluation metrics**: MAE, RMSE, Pearson r.
- **Preprocessing assumptions**: Dynamic spatial-temporal face tracking to compensate for requested head motions; frame difference calculation (if required by model).

### 3. VIPL-HR
- **Frame rate**: Varied (~25-30 fps).
- **Labels**: BVP (Blood Volume Pulse) signal.
- **Heart-rate annotations**: Ground truth heart rate (BPM), SpO2.
- **Evaluation metrics**: MAE, RMSE, Pearson r.
- **Preprocessing assumptions**: Highly compressed video sequences with varying illumination and massive head movements; requires robust spatial tracking and compression artifact mitigation.
