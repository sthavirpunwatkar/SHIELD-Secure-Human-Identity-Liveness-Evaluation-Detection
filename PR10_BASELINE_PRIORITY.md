# SHIELD PR-010D: Baseline Prioritization & Recommendations

## PART 4 — BASELINE PRIORITIZATION

### Top 5 Anti-Spoof Baselines
1. **CDCN (Central Difference Convolutional Networks)**
   - *Reason*: High citation count, widely recognized as a benchmark standard in academia, reliable public weights, PyTorch native.
2. **Silent-Face-Anti-Spoof (MiniFASNet)**
   - *Reason*: Extremely popular in practical/edge deployments, well-known baseline for real-time performance, open weights.
3. **DeepPixBiS**
   - *Reason*: Strong pixel-wise supervision baseline, easily reproducible, solid academic foundation.
4. **Meta-FAS**
   - *Reason*: Excellent representative of domain-generalization and cross-dataset testing standards.
5. **CDCN++**
   - *Reason*: Natural evolution of CDCN; provides a slightly stronger bound on performance while sharing the same integration overhead.

### Top 5 rPPG Baselines
1. **RhythmMamba**
   - *Reason*: AAAI 2025 SOTA. Highly efficient (linear complexity SSM), proving it can compete with ViTs but run much faster. Excellent modern baseline.
2. **PhysNet**
   - *Reason*: Foundational spatiotemporal CNN baseline; fully integrated into rPPG-Toolbox, making it highly reproducible.
3. **PhysFormer**
   - *Reason*: The definitive Vision Transformer baseline for rPPG. High citation count, sets the standard for attention-based models.
4. **TS-CAN**
   - *Reason*: Strong balance of speed and accuracy; widely evaluated and reproducible via rPPG-Toolbox.
5. **PhysMamba**
   - *Reason*: Another top-tier Mamba-based model demonstrating the current paradigm shift in rPPG from Transformers to SSMs.

---

## PART 5 — RECOMMENDATION

### Anti-Spoofing Recommendations
- **CDCN**: **A (Benchmark against it only)**. *Evidence*: It is older (2020) and computationally heavy compared to modern edge models. Good for academic comparison, bad for production replacement.
- **Silent-Face-Anti-Spoof (MiniFASNet)**: **B (Fine-tune it later)**. *Evidence*: Ultra-fast and lightweight. If SHIELD is too slow on edge devices, this architecture is worth adapting.
- **DeepPixBiS**: **A (Benchmark against it only)**. *Evidence*: Good for pixel-wise metrics but architecture is older.
- **Meta-FAS**: **A (Benchmark against it only)**. *Evidence*: Only useful to prove SHIELD's cross-domain generalization.
- **CDCN++**: **A (Benchmark against it only)**. *Evidence*: Same as CDCN.

### rPPG Recommendations
- **RhythmMamba**: **C (Potentially replace the current model)**. *Evidence*: State-of-the-art SSM approach (2025). Extremely fast and memory efficient. If benchmark evidence demonstrates statistically significant improvement over SHIELD, the Mamba architecture is the optimal upgrade path.
- **PhysNet**: **A (Benchmark against it only)**. *Evidence*: 2019 architecture. Historically significant but surpassed in both accuracy and speed by modern SSMs.
- **PhysFormer**: **A (Benchmark against it only)**. *Evidence*: Computationally heavy (ViT). High GPU memory usage makes it unsuitable for efficient production unless accuracy is vastly superior (which Mamba now challenges).
- **TS-CAN**: **B (Fine-tune it later)**. *Evidence*: Highly efficient. If SHIELD struggles with temporal modeling under severe compute constraints, TS-CAN is a proven fallback.
- **PhysMamba**: **C (Potentially replace the current model)**. *Evidence*: Similar to RhythmMamba, SSMs represent the current SOTA frontier for rPPG.

---

## FINAL DECISION

**1. Immediate benchmark candidates**
*(Models with pretrained weights that can be evaluated immediately via adapter scripts)*
- **FAS**: CDCN, Silent-Face-Anti-Spoof (MiniFASNet)
- **rPPG**: PhysNet, TS-CAN

**2. Fine-tuning candidates**
*(Models worth adapting only if SHIELD underperforms)*
- **FAS**: Silent-Face-Anti-Spoof (MiniFASNet) (for speed)
- **rPPG**: TS-CAN (for efficient temporal attention)

**3. Replacement candidates**
*(Models that should only be considered if benchmark evidence demonstrates a statistically significant improvement)*
- **FAS**: None. (No surveyed model offers a generational leap over current SOTA production architectures without severe compute penalties).
- **rPPG**: RhythmMamba, PhysMamba. (The shift to State Space Models / Mamba offers a generational improvement in the accuracy-to-compute ratio for long-range sequence modeling).
