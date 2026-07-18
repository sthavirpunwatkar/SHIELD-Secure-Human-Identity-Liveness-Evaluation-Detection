# SHIELD PR-010D: Execution Plan & Model Matrix

## PART 6 — EXECUTION PLAN

| Model | Paper | Year | Dataset | Parameters | FPS | License | Framework | Weights Available | GitHub | Benchmark Ready (Yes/No) | Reason |
|-------|-------|------|---------|------------|-----|---------|-----------|-------------------|--------|-------------------------|--------|
| **MiniFASNet** | Silent Face Anti-Spoofing | 2019 | CASIA-SURF | ~1-3M | 500+ | MIT | PyTorch/NCNN | Yes | minivision-ai/Silent-Face-Anti-Spoofing | No | Different input size (80x80) and ROI expansion. |
| **CDCN** | Searching Central Difference Convolutional Networks | 2020 | OULU-NPU | ~3M | ~30 | Apache 2.0 | PyTorch | Yes | ZitongYu/CDCN | No | Different tensor shape (256x256), custom MTCNN crop. |
| **CDCN++** | Searching Central Difference Convolutional Networks | 2020 | OULU-NPU | ~4.5M | ~28 | Apache 2.0 | PyTorch | Yes | ZitongYu/CDCN | No | Same as CDCN. |
| **DeepPixBiS** | Deep Pixel-wise Binary Supervision... | 2019 | OULU-NPU | ~15M | ~60 | MIT | PyTorch | Yes | lucasb-eyer/DeepPixBiS | No | Different input resolution (224x224). |
| **DeepPhys** | DeepPhys: Video-Based Physiological Measurement... | 2018 | UBFC/AFRL | ~1-2M | 100+ | MIT | PyTorch | Yes | ubicomplab/rPPG-Toolbox | No | Requires motion & appearance normalized frame differences. |
| **PhysNet** | Remote Photoplethysmograph Signal Measurement... | 2019 | VIPL-HR | ~1-2M | ~50 | MIT | PyTorch | Yes | ubicomplab/rPPG-Toolbox | No | Requires T=64 sliding window and 128x128 resize. |
| **PhysFormer** | PhysFormer: Facial Video-based Physiological Measurement | 2022 | PURE/UBFC | ~20M | ~15 | Apache 2.0 | PyTorch | Yes | ZitongYu/PhysFormer | No | T=160 window, specific face tracking required. |
| **TS-CAN** | TS-CAN | 2020 | AFRL | ~2-3M | 100+ | MIT | PyTorch | Yes | xliu0/ts-can | No | Frame difference preprocessing, 72x72 input. |
| **RhythmMamba** | RhythmMamba: Fast Remote Physiological Measurement... | 2025 | PURE/UBFC | ~5-10M | 200+ | MIT | PyTorch | Yes | zizheng-guo/RhythmMamba | No | Requires State Space Model compatible tensor layout. |
| **PhysMamba** | PhysMamba: Efficient Remote Physiological Measurement... | 2024 | PURE/VIPL | ~5-10M | 150+ | Apache 2.0 | PyTorch | Yes | JasonYpro/PhysMamba | No | Requires dual-stream temporal difference inputs. |

### Implementation Roadmap
1. **No SHIELD Modification:** SHIELD is frozen. All benchmarking runs on the unmodified harness.
2. **Adapter Layer Strategy:** The benchmark harness must implement model-specific adapter classes to intercept SHIELD's default tensor and apply specific preprocessing (resizing, retemporalizing, normalizing) required by the target SOTA model.
3. **Weight Acquisition:** Download official `.pth` weights for Immediate Benchmark Candidates (e.g., CDCN, MiniFASNet, PhysNet, TS-CAN).
4. **Execution Protocol:** Feed standardized dataset cohorts through the adapter-wrapped baselines.
5. **Data Extraction:** Export baseline metrics strictly for comparison. These models remain strictly out-of-tree dependencies and are NOT merged into SHIELD.
