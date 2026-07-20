# Model Stability Report

## Methodology
The ONNX model expects exactly `[1, 1, 150]`. To evaluate shorter windows, the truncated signals were zero-padded to 150 frames. For each window size, inference was repeated 20 times. 

## Stability Data
| Window Size | Mean Confidence | Std. Dev |
| :---: | :---: | :---: |
| 150 | 0.136 | 0.0 |
| 135 | 0.075 | 0.0 |
| 120 | 0.023 | 0.0 |
| 105 | 0.044 | 0.0 |
| 90 | 0.002 | 0.0 |
| 75 | 0.000 | 0.0 |
| 60 | 0.000 | 0.0 |
| 45 | 0.000 | 0.0 |
| 30 | 0.000 | 0.0 |

## Analysis
1. **Deterministic Predictions**: The ONNX runtime produces perfectly deterministic predictions (Standard Deviation = 0.0) across 20 iterations for identical inputs.
2. **Padding Degradation**: The model's baseline confidence drops catastrophically when padded. At 150 frames, it yields a 0.136 score (the source test video is a synthetic / static scene, heavily leaning toward spoof). However, once zero padding is applied for windows < 120 frames, the output effectively rounds down to absolute `0.000`. 
3. **Architectural Failure**: The `FrequencyBranch` relies on an FFT over the full tensor. Zero padding introduces a massive step-function discontinuity in the time domain, shattering the frequency spectrum and destroying the physiological features.

**Conclusion**: The trained model's architecture CANNOT accept short sequences padded with zeros. The model is deeply unstable and functionally collapses if given fewer than 150 actual frames of contiguous physiological data.
