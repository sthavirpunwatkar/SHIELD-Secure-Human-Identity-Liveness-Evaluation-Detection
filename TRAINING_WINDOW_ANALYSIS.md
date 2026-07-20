# Training Pipeline Audit: rPPG Temporal Requirements

## Overview
This document audits the training pipeline for the `RPPGCNNv2` model (`train_rppg_v2.py` and `rppg_dataset.py`) to determine whether the 150-frame requirement is a deliberate architectural property or an arbitrary implementation detail.

## Training Parameters
- **Training FPS**: 30 FPS
- **Window Size**: 150 frames
- **Sequence Length**: 150 frames
- **Sampling Strategy**: 
  - Real Videos: Extracted as sliding windows from green-channel ROI.
  - Synthetic Data: Physics-based generation combining cardiac sine waves, respiratory modulation, random walk motion artifacts, and Gaussian noise.
- **Stride / Overlap**: Stride of `window_size // 2` (75 frames) for real datasets, or a stride of 1 frame (149 frames overlap) for video scanning buffers.
- **Padding**: **None.** All training sequences strictly require and output exactly 150 valid frames. 
- **Normalization**: Z-score normalization applied per-window: `(signal - mean) / (std + 1e-6)`.
- **Filtering**: 2nd-order Butterworth bandpass filter (0.7 Hz to 4.0 Hz).
- **Signal Duration**: 5.0 seconds.
- **Model Input Shape**: `(BatchSize, 1, 150)`

## Analysis: Why was 150 frames chosen?
The choice of 150 frames (5.0 seconds at 30 FPS) is rooted in biological constraints for frequency-domain heart rate estimation:
1. **Cardiac Periodicity**: Normal human resting heart rate is between 60 and 100 Beats Per Minute (BPM), which equates to 1.0 to 1.66 Hz.
2. **Frequency Resolution**: To accurately distinguish a cardiac signal using the Fast Fourier Transform (FFT) in the `FrequencyBranch` of the network, a multi-second window is biologically necessary to capture multiple complete cardiac cycles (at least 4 to 8 beats). 
3. **Hardcoded Architecture**: The `FrequencyBranch` statically expects a fixed FFT output size of `window_size // 2 + 1` (76 bins), feeding into a rigid Multi-Layer Perceptron (MLP). The network was fundamentally designed, trained, and structurally locked to a 5-second duration.
