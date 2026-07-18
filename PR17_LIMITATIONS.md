# PR-017: Validation Limitations

When reviewing the benchmark output artifacts, the following strict limitations apply:

1. **Subset Restriction:** Only a synthetic, highly localized mock subset mimicking the file structure of external datasets was evaluated due to access restrictions and time constraints.
2. **No Retraining:** External baselines (MiniFASNet, PhysNet) executed their default open-source weights out-of-the-box. They were explicitly **not** fine-tuned to SHIELD's internal distributions.
3. **Frozen Environment:** The SHIELD production pipeline remained frozen. No fusion logic or backend inference thresholds were tuned in response to these metrics.
4. **Scope of Conclusion:** These results empirically validate the robust engineering of the benchmark framework itself (data loading, preprocessing parity, metric generation). However, the absolute metric values (e.g. `AUC`, `ACER`) represent structural testing outcomes and should not be used to definitively state one model is algorithmically superior without running over the complete, non-synthetic multi-terabyte dataset schemas on a GPU cluster.
