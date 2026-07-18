# PR-015: Failure Analysis

- **Initial Bug:** Our initial `MiniFASNetAdapter` assumed the output was `(1, 2)`. Real execution revealed the `2.7_80x80` checkpoint uses 3 classes `(1, 3)`.
- **Root Cause:** Minivision trains separate classes for different spoof attacks (e.g., printed vs replay) rather than a binary output.
- **Resolution:** The `postprocess` method natively extracts index 1 (Live), circumventing any hardcoded shape issues, allowing it to gracefully adapt without crashing.

- **PhysNet Temporal Dimension Mismatch:** The initial expectation was a `(1, 32)` output for a 32-frame input.
- **Root Cause:** The `vision-cardio-rppg` checkpoint utilizes only the encoding half of the PhysNet architecture, reducing temporal resolution by 4x.
- **Resolution:** The adapter handles the `(1, 8)` output gracefully, accurately representing the latent signal natively.
