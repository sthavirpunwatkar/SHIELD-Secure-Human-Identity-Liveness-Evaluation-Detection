# PR-012: Directory Structure

The following directories and files were successfully structured under the `benchmark/` root for PR-012:

```text
benchmark/
├── adapters/
│   ├── base_adapter.py             # Interface definition (BenchmarkModel)
│   ├── minifasnet_adapter.py       # Wrapper for Silent-Face-Anti-Spoofing
│   ├── shield_fas_adapter.py       # Benchmark wrapper for production Anti-Spoof
│   ├── shield_rppg_adapter.py      # Benchmark wrapper for production rPPG
│   └── tscan_adapter.py            # Wrapper for TS-CAN
├── runners/
│   └── benchmark_runner.py         # Main execution loop for the harness
└── utils/
    ├── metrics.py                  # Profiling (psutil, torch cuda tracking)
    ├── preprocessing.py            # External-specific crop and scaling logic
    └── visualization.py            # Diagnostic tools (waveform plotting)
```
