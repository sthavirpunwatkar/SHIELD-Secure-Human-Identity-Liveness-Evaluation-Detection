# PR-016: Failure Analysis

## Simulated Disagreements & Probable Causes

### 1. Mobile Replay Attacks
- **Observation:** SHIELD successfully identified the presentation attack, while MiniFASNet predicted `LIVE`.
- **Probable Cause:** MiniFASNet's official V2 weights might over-index on facial geometry and lack robustness against high-resolution screen moiré patterns or specific digital spoof mediums not heavily emphasized in its training set, resulting in a false positive.

### 2. Complex Lighting
- **Observation:** SHIELD occasionally defaulted to `SPOOF` while MiniFASNet predicted `LIVE`.
- **Probable Cause:** Highly simulated noise/low illumination degraded the input tensor. If SHIELD's preprocessing relies on strict illumination thresholds for its fusion logic, it fails gracefully (safe), whereas the CNN architecture of MiniFASNet forces a classification output regardless of image degradation.

## Data Artifacts
Original frames, detected crops, and visualizations for these outputs are programmatically retrievable from the synthetic dataset matrix.
