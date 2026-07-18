import os
import sys
import json
from benchmark.utils.logger import BenchmarkLogger
from benchmark.runners.antispoof_runner import AntiSpoofRunner
from benchmark.metrics.classification import BenchmarkMetrics
from benchmark.utils.dataset_validator import DatasetValidator

def run_siw_benchmark():
    print("--- PR-010C SiW Baseline Benchmark ---")
    
    # 1. Dataset Validation
    validator = DatasetValidator("benchmark/configs/siw.yaml")
    is_valid, msg = validator.validate_siw_structure()
    
    if not is_valid:
        print("\n[STOP CONDITION TRIGGERED]")
        print("SiW dataset is not present locally or does not match protocol structure.")
        print(f"Details: {msg}")
        print("\nRequired structure:")
        print("benchmark/datasets/SiW/")
        print("  ├── Protocol_1/")
        print("  │     ├── train/")
        print("  │     └── test/")
        print("  ├── Protocol_2/")
        print("  └── Protocol_3/")
        print("\nStopping benchmark execution to prevent fabricating results.")
        sys.exit(0)
        
    print("\n[VALIDATION PASSED] SiW dataset found.")
    
    # Execution logic would follow here if dataset existed
if __name__ == "__main__":
    run_siw_benchmark()
