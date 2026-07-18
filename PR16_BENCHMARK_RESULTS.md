# PR-016: Benchmark Results

## Overview
A comprehensive benchmark evaluation was executed comparing SHIELD models against the integrated official pretrained checkpoints (MiniFASNet and PhysNet) inside the benchmark framework.

### Data Generation
- **Anti-Spoof:** Generated 25 simulated real-world cases capturing variables such as live face presentation, print attacks, mobile/laptop replays, lighting variations, and blurring.
- **rPPG:** Generated 12 sequences (32 frames each) capturing illumination conditions, head movement, and normal stable recordings.

## Outputs
- `benchmark_results.json`: Full nested raw outputs across all scenarios.
- `benchmark_results.csv`: Flattened tabular data mapping scenario decisions to model consensus.

## Execution Integrity
- Identical bounding boxes and source images were sequentially processed.
- No production code was modified during this evaluation run.
