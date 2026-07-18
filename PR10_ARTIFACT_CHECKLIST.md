# SHIELD PR-010F: Artifact Archival Checklist

For absolute reproducibility, the following artifacts **MUST** be present in the output directory and archived permanently after every benchmark execution.

## Raw Logs and Outputs
- [ ] `predictions.jsonl`: Raw inference outputs for every sample (Filename, True Label, Predicted Score).
- [ ] `benchmark.log`: Complete capture of `stdout` and `stderr` during harness execution.

## Environment Documentation
- [ ] `system_info.json`: Snapshot of OS, Kernel, CUDA, Python, and hardware details.
- [ ] `git_commit.txt`: Output of `git rev-parse HEAD` and `git diff` to guarantee harness state.
- [ ] `model_checksums.json`: SHA256 hashes of the dataset manifest and model weights used.

## Analytical Outputs
- [ ] **Markdown Report**: A completed `PR10_RESULTS_TEMPLATE.md` with all fields filled.
- [ ] **Plots**:
  - [ ] `roc_curve.png` or equivalent ROC plot.
  - [ ] `confusion_matrix.png` or equivalent CM plot.
  - [ ] `score_histograms.png` or equivalent metric distribution histograms.
