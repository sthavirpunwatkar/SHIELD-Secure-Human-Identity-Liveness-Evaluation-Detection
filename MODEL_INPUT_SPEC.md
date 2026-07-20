# ONNX Model Input Specification

## Overview
Inspection of the exported ONNX graph (`models/rppg_1dcnn_v2.onnx`) defines the strict mathematical expectations of the inference engine. 

## Tensor Properties
- **Input Name**: `rppg_signal`
- **Required Tensor Shape**: `[1, 1, 150]` (Batch, Channel, Sequence)
- **Static vs Dynamic Dimensions**: **Strictly Static.** The ONNX exporter was run without dynamic axes. The input sequence length is hardcoded to `150`.
- **Sequence Axis**: Axis 2 (the 3rd dimension).
- **Padding Assumptions**: The ONNX model makes **zero padding assumptions**. It mathematically assumes that every single element in the `150` length sequence represents a valid, continuous, physiologically captured sequence of measurements. Because the internal `FrequencyBranch` relies on an FFT over the entire window, zero-padding shorter sequences fundamentally changes the frequency spectrum and corrupts the structural integrity of the temporal features. 

## Conclusion
The `RPPGCNNv2` ONNX model cannot natively support streaming inputs or dynamically sized sequences. It strictly requires exactly 150 frames of continuous data.
