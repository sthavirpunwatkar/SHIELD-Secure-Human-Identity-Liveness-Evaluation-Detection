# PR-011: Integration Plan

## Objective
To outline the step-by-step process for introducing the external pretrained models into the SHIELD benchmarking environment, strictly adhering to the "No Production Modification" mandate.

## Phase A: Environment Preparation
1. **Isolate Dependencies:** 
   * Create an isolated Python virtual environment specifically for the benchmark harness to prevent dependency pollution.
   * Do not touch the `requirements-prod.txt` used by SHIELD.
2. **Directory Structure:** 
   * Create a new directory within the testing suite: `tests/benchmarks/external_models/`.
   * Under this directory, create subdirectories for `minifasnet` and `tscan`.

## Phase B: Adapter Implementation
1. **Implement `MiniFASNetAdapter`:**
   * Author `tests/benchmarks/external_models/minifasnet/adapter.py`.
   * Implement the transformation logic specified in `PR11_ADAPTER_SPECIFICATION.md`.
2. **Implement `TSCANAdapter`:**
   * Author `tests/benchmarks/external_models/tscan/adapter.py`.
   * Implement the temporal buffering and tensor formatting.

## Phase C: Harness Registration
1. **Dependency Injection:** 
   * Register the new adapters within the benchmark test suite config (e.g., `benchmark_config.yaml`), ensuring they are instantiated *only* when the benchmarking flag `--run-external-baselines` is invoked.
2. **Test the Wrappers:**
   * Pass dummy noise tensors through the adapters to ensure they do not crash and that they correctly map dummy inputs to the expected `BenchmarkResult` output format.

## Phase D: Dry Run and Verification
1. **Execute Benchmark on Sandbox Data:**
   * Run the SHIELD benchmark harness with a small subset of test data.
   * Verify that SHIELD's internal performance metrics (latency, memory usage) remain completely unaffected by the presence of the external models in the test suite.
2. **Validate Read-Only Guarantee:**
   * Ensure the adapter does not modify the original image pointers or mutate the system context.
3. **Commit:**
   * Open PR-011 containing only the benchmark logic, wrappers, and documentation. No production files should be present in the diff.
