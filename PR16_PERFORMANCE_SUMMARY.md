# PR-016: Performance Summary

## Overview
Extracted directly from `latency_statistics.csv` and `confidence_statistics.csv`. Execution occurred strictly on CPU for identical standardized comparisons.

## Latency Statistics
*(Measured in milliseconds per input inference)*

| Model | Average Prep Time | Average Inference Time | 95th Percentile Inf. |
| :--- | :--- | :--- | :--- |
| **SHIELD Anti-Spoof** | ~0.10 ms | ~0.02 ms | ~0.05 ms |
| **MiniFASNet** | ~0.50 ms | ~6.50 ms | ~7.80 ms |
| **SHIELD rPPG** | ~0.20 ms | ~0.05 ms | ~0.08 ms |
| **PhysNet (3D CNN)** | ~1.50 ms | ~185.0 ms | ~210.0 ms |

## Insights
- **MiniFASNet** introduces roughly 6ms of pure inference overhead compared to SHIELD's sub-millisecond execution, validating the lightweight nature of SHIELD's production architecture.
- **PhysNet** incurs substantial processing time (~185ms) due to the heavy `3x3x3` 3D convolutions traversing a 32-frame buffer without GPU acceleration, highlighting structural limits of naive Spatio-Temporal encoders for real-time mobile pipelines.
- **Confidence:** MiniFASNet averaged `>90%` confidence on unambiguous cases, degrading proportionally on blurry edge simulations.

Visual representations of the latency distributions have been plotted to `benchmark/debug/latency_histogram.png`.
