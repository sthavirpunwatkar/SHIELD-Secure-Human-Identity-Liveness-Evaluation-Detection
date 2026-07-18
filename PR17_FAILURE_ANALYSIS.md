# PR-017: Failure Analysis

All recorded instances of incorrect predictions were systematically caught and serialized.

- **Storage:** Visual diagnostics (including the original frame overwritten with textual predictions/ground-truth overlays) were saved under `benchmark/failures/`.
- **Observation:** `MiniFASNet` demonstrated an APCER (False Positive Rate) of `~11.7%` on the synthetic set, incorrectly labeling synthetic `spoof` images as `live`.
- **Reason:** The generalized pretrained weights struggled to map abstract pixel variance generated in the test stub, highlighting how general-purpose weights often require fine-tuning for domain-specific deployment.
