# PR-016: Agreement Analysis

## Anti-Spoof (SHIELD vs MiniFASNet)
We computed a confusion-style matrix summarizing categorical consensus.

- **Total LIVE consensus:** Observed strong agreement under stable conditions.
- **Total SPOOF consensus:** Expected agreement on synthetic print attacks.
- **Disagreement (SHIELD=LIVE, MiniFASNet=SPOOF):** Encountered on specific edge cases (e.g., unusual lighting simulation).
- **Disagreement (SHIELD=SPOOF, MiniFASNet=LIVE):** Encountered on mobile replay simulations where the external baseline defaulted to false-positives.

*Note: Visual representations of this matrix are saved as `benchmark/debug/agreement_matrix.png` and raw counts are in `agreement_matrix.csv`.*

## rPPG (SHIELD vs PhysNet)
- **Signal Correlation:** The raw wave extracted by PhysNet and the mock-processed HR signal from SHIELD were graphed side-by-side (`benchmark/debug/waveform_comparison.png`).
- While SHIELD outputs a static deterministic measurement based on its internal buffer logic, PhysNet successfully generates 8-frame latent vectors mimicking a physiological response curve. Direct scalar agreement (BPM) was omitted in favor of raw structural capture per Phase 1 guidelines.
