# PR-014: Validation Report

## Overview
A validation smoke test was executed using `benchmark_runner.py` to ensure `PhysNet` correctly instantiated from the downloaded checkpoint and that the pipeline executed without TensorFlow.

## Sanity Check Results

- [x] **Checkpoint Loads:** `rppg_physnet_ubfc.pt` loaded successfully into the custom `PhysNet` PyTorch module.
- [x] **Inference Executes:** The 3D CNN successfully consumed a `(1, 3, 32, 128, 128)` sequence tensor and outputted the predicted signal.
- [x] **Outputs Decode Correctly:** The raw waveform was averaged across spatial dimensions and evaluated for pseudo heart-rate mapping.
- [x] **Latency Measured:** End-to-end execution of the 3D-CNN forward pass was successfully timed and recorded.
- [x] **Logs Generated:** `timings.csv` and `predictions.jsonl` dynamically tracked `PhysNet` alongside `MiniFASNet`.

## Success Criteria Verification
The integration fulfills all PR-014 requirements:
- ✅ SHIELD Anti-Spoof runs (via wrapper)
- ✅ MiniFASNet runs (real inference)
- ✅ SHIELD rPPG runs (via wrapper)
- ✅ PhysNet runs (PyTorch-native real inference)
- ✅ TensorFlow was **not** introduced.
- ✅ SHIELD production code was **not** modified.
