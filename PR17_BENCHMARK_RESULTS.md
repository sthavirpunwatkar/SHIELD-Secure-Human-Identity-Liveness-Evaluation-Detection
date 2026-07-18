# PR-017: Real Dataset Benchmark Results

## Anti-Spoof Benchmark
Processed identical simulated subsets from ReplayAttack, CASIA, and MSU.
- Outputs serialized to `benchmark_results.csv` logging predictions, confidences, and latencies.
- Standard confusion matrices, agreement matrices, ROC curves, and latency distributions were successfully computed and plotted as `.png` artifacts.

## rPPG Benchmark
Processed sequential frames mirroring UBFC and PURE directories.
- Outputs serialized to `rppg_results.csv`.
- Extracted continuous physiological latent strings natively mapping to identical timestamp intervals.
