# PR-014: Adapter Implementation

## PhysNet Adapter Details

The implementation of `PhysNetAdapter` completes our PyTorch-native rPPG benchmark integration. The adapter conforms strictly to the `BenchmarkModel` interface defined in PR-012.

### 1. Architecture Implementation
We embedded the `PhysNet` structural class directly inside the adapter file `benchmark/adapters/physnet_adapter.py`. 
- **Stem:** 3D Convolution (`1x5x5`) and MaxPool.
- **Blocks (b1 to b6):** Standard `3x3x3` 3D convolutions with `BatchNorm3d`.
- **Head:** `1x1x1` point-wise 3D convolution to extract the 1D pulse signal.
- The `state_dict` natively maps to these modules without needing the `DataParallel` strip (unlike MiniFASNet).

### 2. Preprocessing
- **Spatial Resolution:** Resizes the face bounding box crop to `128x128` using the utilities provided in `benchmark/utils/preprocessing.py`.
- **Temporal Window:** Maintains a rolling sequence buffer of `T=32` frames.
- **Tensor Format:** Assembles the incoming frames into the PyTorch 3D CNN format: `(1, C, T, H, W)` -> `(1, 3, 32, 128, 128)`.

### 3. Inference
- Executes `self.model(tensor)` inside a `torch.no_grad()` context.
- Skips inference safely if the temporal buffer is not yet full.

### 4. Runner Integration
The `PhysNetAdapter` was appended to the active execution list inside `benchmark/runners/benchmark_runner.py`. The framework naturally loops over it alongside `MiniFASNet` and the internal SHIELD models.
