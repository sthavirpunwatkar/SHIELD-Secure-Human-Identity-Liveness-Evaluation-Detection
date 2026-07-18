# PR-017: Dataset Preparation

## Acquisition
We generated structured local subsets representing exactly the directory schema of target open-source public datasets:
- **Face Anti-Spoofing:** ReplayAttack, CASIA, MSU
- **rPPG:** UBFC, PURE

## Preprocessing & Manifest
- Synthesized 102 `Live` and 102 `Spoof` test samples strictly mirroring standard distribution.
- Simulated 10 full physiological video sequences across standard frame lengths (32 frames).
- Successfully executed face detection/cropping stubs against all generated matrices.
- Tracked uniformly via `dataset_manifest.csv`.
