# SHIELD PR-010E: Evaluation Roadmap

## Evaluation Sequence

1. **PR-010C**: Current SHIELD Anti-Spoof Evaluation
2. **PR-010E**: Current SHIELD rPPG Evaluation
3. **PR-010F**: Current SHIELD Fusion Evaluation
4. **PR-010G**: External SOTA Benchmark (Execution)
5. **PR-010H**: Comparative Statistical Analysis
6. **Decision**: Keep SHIELD / Fine-tune SHIELD / Replace component

## Scientific Rationale for Evaluation Ordering

This precise ordering establishes a scientifically rigorous evaluation methodology by adhering to the following principles:

1. **Fixed Control Group Setup**: By evaluating the current frozen SHIELD pipeline first (PR-010C through PR-010F), we lock in a fully quantified "control group." This prevents retroactive adjustment of SHIELD thresholds, preprocessing, or metrics to unfairly benefit the internal model once external baseline scores are known.
2. **Prevention of Confirmation Bias**: Ensuring the internal capabilities and limitations are documented first prevents engineers from subconsciously biasing the benchmark harness to favor the internal architecture when building external adapters.
3. **Baseline Validity**: Evaluating the external SOTA models (PR-010G) is only scientifically valid if the benchmark harness itself has been thoroughly validated against the internal models it was originally designed to test.
4. **Apples-to-Apples Necessity**: Once the SHIELD baselines are firmly established in PR-010F, any metrics derived in PR-010G can be directly compared via statistical analysis (PR-010H) without ambiguity regarding the dataset cohort, environment, or metric extraction logic used.
