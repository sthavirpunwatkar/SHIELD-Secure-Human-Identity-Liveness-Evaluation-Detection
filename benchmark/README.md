# SHIELD Offline Benchmark Harness

This module contains the infrastructure to scientifically evaluate the production inference models against standardized public datasets.

## Structure
* `datasets/`: Mount point or symlinks for downloaded public datasets (e.g., SiW, OULU-NPU).
* `runners/`: Evaluators that wrap the individual inference components without altering their production logic.
* `metrics/`: Centralized metric computation logic (ROC, EER, APCER).
* `visualization/`: Helper functions to generate graphs.
* `configs/`: YAML definitions parameterizing datasets.
* `outputs/`: Automatically generated timestamped folders containing predictions, logs, and system metadata.
* `utils/`: Common utilities such as the `BenchmarkLogger`.

## Constraints
* **FROZEN INFERENCE:** This harness **must not** modify or retrain the models in `../inference/`. It treats them strictly as black boxes.
* **OFFLINE ONLY:** This framework is designed for offline benchmarking on local disk data, simulating the frontend camera streams.
