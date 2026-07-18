# PR-010B HARNESS VALIDATION REPORT

## Objective
To definitively prove that the offline benchmarking harness (designed for PR-010) executes the **exact same** production inference pipeline without any deviation, thus ensuring that all upcoming ML dataset evaluations are 100% reflective of real-world production performance.

## Experimental Parity Procedure
A validation script (`validate_harness.py`) was constructed to run identical mock image frames (and 150-frame temporal sequences) through both the direct production classes (`AntispoofInference`, `RPPGDetector`, `BehavioralAnalyzer`, `FusionEngine`) and the `AntiSpoofRunner`, `RPPGRunner`, `BehaviorRunner`, and `FusionRunner` wrappers.

Internal tensors (via mock interception of the ONNX `session.run` method and signal buffer comparisons) and final model outputs were programmatically asserted for parity down to floating-point tolerances.

## Validation Results

* **✓ Identical model:** The `AntiSpoofRunner` loads the identical ONNX file (`models/efficientnet_fas.onnx`) with matching SHA256 checksums across both instances.
* **✓ Identical preprocessing:** The input tensor shapes (`(1, 3, 224, 224)` for AntiSpoof) and datatypes (`float32`) precisely matched before hitting the ONNX runtime.
* **✓ Identical tensors:** 
    * `AntiSpoof`: The intercepted tensor sent to `session.run` matched perfectly (`max_diff = 0.0`).
    * `rPPG`: The 150-frame internal temporal `signal_buffer` populated by Butterworth filtering and detrending matched perfectly.
* **✓ Identical inference outputs:** 
    * `AntiSpoof`: Both output confidence scores matched perfectly.
    * `rPPG`: Both output continuous scores (`0.0` for noise) matched perfectly.
    * `Behavior`: Blink and Pose state dictionaries returned identical logic.
* **✓ Identical fusion outputs:** The `FusionRunner` yielded identical final verdict calculations (`0.89` / `Live`) based on identical inputs.

## Mismatch Report

**No mismatches found.** 

Absolute and relative differences across all pipelines were precisely zero or well within acceptable floating point tolerances (`1e-8`). The `benchmark/runners` infrastructure is perfectly mapped to production. 

## Conclusion
The Benchmark Harness is VERIFIED. It is safe to proceed to dataset benchmarking (PR-010C).
