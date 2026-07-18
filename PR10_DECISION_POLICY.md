# SHIELD PR-010E: Decision Policy

## Core Mandate
External models may **ONLY** be recommended if they demonstrate a statistically significant improvement over the established SHIELD production baselines.

- **NO** subjective recommendations.
- **NO** architectural opinions (e.g., "Mamba is newer than ViT, so we should switch").
- **EVERY** recommendation must explicitly cite measured benchmark evidence (e.g., p-values, relative error reduction, FPS variance under identical load).

## Permissible Outcomes

Upon completion of the Comparative Statistical Analysis (PR-010H), the following outcomes are the only valid paths forward:

### A. Keep current SHIELD model.
- **Condition**: The external SOTA models do not yield a statistically significant improvement over SHIELD in primary accuracy metrics (e.g., ACER, MAE), or any marginal accuracy gains are negated by unacceptable latency, memory overhead, or cross-dataset generalization collapse.
- **Action**: The production pipeline remains completely frozen as is.

### B. Fine-tune current SHIELD model.
- **Condition**: The external SOTA models demonstrate superior performance in specific edge cases (e.g., dark illumination in OULU-NPU, heavy motion in PURE), but the SHIELD architecture remains computationally superior.
- **Action**: Propose a subsequent PR to fine-tune the *existing* frozen SHIELD model on targeted data slices to close the performance gap without adopting the external architecture.

### C. Replace current SHIELD model.
- **Condition**: An external SOTA model demonstrates a statistically significant improvement (e.g., lower ACER, lower MAE) across multiple datasets **AND** meets or exceeds all production constraints regarding latency, memory footprint, and license compatibility.
- **Action**: Propose a completely new engineering initiative to rewrite the SHIELD component utilizing the new architecture. 

*Any outcome recommended MUST directly quote the `predictions.jsonl` variance and the finalized metric calculation derived from the PR-010G benchmark run.*
