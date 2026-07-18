# SHIELD PR-010F: Benchmark Execution Runbook

## Standardized Execution Procedure

### 1. Environment Verification
- [ ] Verify identical base OS and kernel version across benchmark runs.
- [ ] Record CUDA, cuDNN, and GPU driver versions (`nvidia-smi` output).
- [ ] Ensure all python dependencies exactly match the frozen `requirements.txt`.
- [ ] Confirm random seeds for `numpy`, `torch`, and `random` are explicitly set and logged.

### 2. Dataset Verification
- [ ] Confirm the target dataset directory exists and matches the expected schema.
- [ ] Compute the SHA256 checksum of the dataset manifest/index.
- [ ] Ensure the checksum strictly matches the trusted dataset cryptographic registry.

### 3. Model Verification
- [ ] Locate the required model weight file (e.g., `.pth`, `.onnx`).
- [ ] Compute the SHA256 checksum of the weight file.
- [ ] Verify the weight checksum matches the official `PR10_MODEL_PROVENANCE_TEMPLATE.md` log.

### 4. Benchmark Execution
- [ ] Ensure no background tasks will interfere with CPU/GPU timing.
- [ ] Execute the frozen benchmark harness via the standard CLI command.
- [ ] Ensure `stdout` and `stderr` are continuously piped to `benchmark.log`.

### 5. Metric Generation
- [ ] Execute the standalone metric calculator on the emitted `predictions.jsonl`.
- [ ] Verify that threshold-independent (AUC) and threshold-dependent (ACER, EER) metrics are computed correctly based on the target protocol.

### 6. Plot Generation
- [ ] Generate standard visualizations (ROC Curve, Confusion Matrix, Error Histograms).
- [ ] Ensure plots are saved as high-resolution PNG/SVG files with proper axis labeling and legends.

### 7. Result Archival
- [ ] Collate all logs, JSON outputs, metric tables, and plots into a timestamped, unique experiment output directory.
- [ ] Update `PR10_EXPERIMENT_REGISTRY.md` with the execution results.
- [ ] Store the output directory in cold-storage or the persistent artifact tracking system.
