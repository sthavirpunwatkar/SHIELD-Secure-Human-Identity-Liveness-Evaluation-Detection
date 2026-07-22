import os
import cv2
import json
import numpy as np
import hashlib

from benchmark.utils.logger import BenchmarkLogger
from benchmark.runners.antispoof_runner import AntiSpoofRunner
from benchmark.runners.rppg_runner import RPPGRunner
from benchmark.runners.behavior_runner import BehaviorRunner
from benchmark.runners.fusion_runner import FusionRunner

from inference.antispoof.inference import AntispoofInference
from inference.rppg_detector import RPPGDetector
from inference.behavioral_analyzer import BehavioralAnalyzer
from inference.fusion_engine import FusionEngine

def assert_tensors_equal(t1, t2, name=""):
    if not np.array_equal(t1, t2):
        if np.allclose(t1, t2, rtol=1e-5, atol=1e-8):
            print(f"[PASS-WITH-TOLERANCE] {name} tensors match within float tolerance.")
        else:
            diff = np.abs(t1 - t2).max()
            raise AssertionError(f"[FAIL] {name} mismatch. Max diff: {diff}")
    else:
        print(f"[PASS] {name} tensors perfectly match.")

def run_validation():
    print("--- BENCHMARK HARNESS VALIDATION ---")
    logger = BenchmarkLogger("parity_test")
    
    # Create synthetic frame (1080p, mimicking production)
    frame = np.random.randint(0, 255, (1080, 1920, 3), dtype=np.uint8)
    face_crop = frame[400:800, 800:1200]  # Random mock crop
    
    # 1. AntiSpoof
    print("\n[1] Validating AntiSpoof...")
    prod_as = AntispoofInference()
    bench_as = AntiSpoofRunner(logger)
    
    from unittest.mock import patch
    
    prod_tensor = []
    def intercept_run_prod(outputs, inputs):
        prod_tensor.append(list(inputs.values())[0])
        return [np.array([[0.9, 0.1]])]
        
    bench_tensor = []
    def intercept_run_bench(outputs, inputs):
        bench_tensor.append(list(inputs.values())[0])
        return [np.array([[0.9, 0.1]])]

    with patch.object(prod_as.session, 'run', side_effect=intercept_run_prod):
        prod_score = prod_as.predict(face_crop)
        
    with patch.object(bench_as.model.session, 'run', side_effect=intercept_run_bench):
        bench_score = bench_as.run_frame(face_crop, {"ground_truth": "live"})
        
    print(f"Shape: {prod_tensor[0].shape}, DType: {prod_tensor[0].dtype}")
    assert_tensors_equal(prod_tensor[0], bench_tensor[0], "AntiSpoof Preprocessing")
    
    print(f"Prod Score: {prod_score} | Bench Score: {bench_score}")
    assert prod_score == bench_score, "AntiSpoof outputs do not match!"
    print("[PASS] AntiSpoof outputs identical.")
    
    # Model Checksum
    with open(prod_as.model_path, "rb") as f:
        prod_hash = hashlib.sha256(f.read()).hexdigest()
    with open(bench_as.model.model_path, "rb") as f:
        bench_hash = hashlib.sha256(f.read()).hexdigest()
    assert prod_hash == bench_hash, "AntiSpoof ONNX models mismatch!"
    print(f"[PASS] AntiSpoof Model Hash: {prod_hash}")

    # 2. rPPG
    print("\n[2] Validating rPPG...")
    prod_rppg = RPPGDetector()
    bench_rppg = RPPGRunner(logger)
    
    # We must feed 150 frames to trigger a score
    score_prod = 0.0
    score_bench = 0.0
    for i in range(150):
        mock_f = np.random.randint(0, 255, (200, 200, 3), dtype=np.uint8)
        score_prod = prod_rppg.update(mock_f)
        score_bench = bench_rppg.run_frame(mock_f, {})
            
    # Check signal buffer parity
    assert_tensors_equal(np.array(prod_rppg.signal_buffer), np.array(bench_rppg.model.signal_buffer), "rPPG Signal Buffer")
    print(f"Prod rPPG: {score_prod} | Bench rPPG: {score_bench}")
    if abs(score_prod - score_bench) > 1e-5:
        print("[FAIL] rPPG outputs differ!")
    else:
        print("[PASS] rPPG outputs identical.")
        
    # 3. Behavior
    print("\n[3] Validating Behavior...")
    prod_beh = BehavioralAnalyzer()
    bench_beh = BehaviorRunner(logger)
    
    res_prod = prod_beh.analyze(frame)
    res_bench = bench_beh.run_frame(frame, {})
    assert res_prod == res_bench, "Behavior outputs do not match!"
    print(f"Outputs: {res_prod}")
    print("[PASS] Behavior outputs identical.")

    # 4. Fusion
    print("\n[4] Validating Fusion...")
    prod_fus = FusionEngine()
    bench_fus = FusionRunner(logger)
    
    res_prod = prod_fus.fuse(0.8, 1.0, 0.9, 0.0, False)
    res_bench = bench_fus.run_fusion(0.8, 1.0, 0.9, 0.0, False, {})
    assert res_prod == res_bench, "Fusion outputs do not match!"
    print(f"Outputs: {res_prod}")
    print("[PASS] Fusion outputs identical.")

    print("\n--- ALL VALIDATIONS PASSED ---")

if __name__ == "__main__":
    run_validation()
