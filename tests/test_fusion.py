import os
import json
import tempfile
import numpy as np
from unittest.mock import MagicMock, patch
from inference.fusion_engine import FusionEngine
from evaluation.tune_weights import WeightTuner

def test_fusion_engine():
    print("--- SHIELD Fusion Engine Test ---")
    engine = FusionEngine()

    # Case 1: High liveness in all components
    print("\nCase 1: Clear Live")
    result = engine.fuse(rppg_score=0.9, behavior_score=1.0, antispoof_score=0.95, challenge_score=1.0)
    print(f"Final Score: {result['final_score']}, Verdict: {result['verdict']}")

    # Case 2: Mixed signals
    print("\nCase 2: Mixed Signals (Possible Spoof)")
    result = engine.fuse(rppg_score=0.2, behavior_score=0.1, antispoof_score=0.3, challenge_score=0.5)
    print(f"Final Score: {result['final_score']}, Verdict: {result['verdict']}")

    # Case 3: Anti-spoof model says real, but physiological says fake
    print("\nCase 3: Physiological Failure (Possible Replay)")
    result = engine.fuse(rppg_score=0.1, behavior_score=0.5, antispoof_score=0.8, challenge_score=0.5)
    print(f"Final Score: {result['final_score']}, Verdict: {result['verdict']}")

    print("\n--- Fusion Engine Test Complete ---")

def test_weight_tuner():
    print("--- SHIELD Weight Tuner Test ---")
    with tempfile.TemporaryDirectory() as tmpdir:
        manifest_path = os.path.join(tmpdir, "manifest.json")
        mock_manifest = [
            {"path": "dummy_live.jpg", "label": "live"},
            {"path": "dummy_spoof.jpg", "label": "spoof"}
        ]
        with open(manifest_path, "w") as f:
            json.dump(mock_manifest, f)
            
        with patch('evaluation.tune_weights.AntispoofInference') as MockAS, \
             patch('evaluation.tune_weights.RPPGDetector') as MockRPPG, \
             patch('evaluation.tune_weights.BehavioralAnalyzer') as MockBehavioral, \
             patch('cv2.imread') as mock_imread:
            
            # Setup mock returns
            mock_imread.return_value = np.zeros((100, 100, 3), dtype=np.uint8)
            
            mock_as_instance = MockAS.return_value
            mock_as_instance.predict.side_effect = [0.9, 0.1]
            
            mock_rppg_instance = MockRPPG.return_value
            mock_rppg_instance.update.side_effect = [0.8, 0.2]
            
            mock_beh_instance = MockBehavioral.return_value
            mock_beh_instance.analyze.side_effect = [
                {"behavior_score": 1.0},
                {"behavior_score": 0.0}
            ]
            
            tuner = WeightTuner(manifest_path)
            weights, acer, accuracy = tuner.tune(min_weight=0.10)
            
            assert weights is not None
            assert "rppg" in weights
            assert "behavior" in weights
            assert "antispoof" in weights
            assert "challenge" in weights
            # Sum of weights must equal 1.0
            assert round(sum(weights.values()), 2) == 1.0
            print("✓ WeightTuner test passed.")

if __name__ == "__main__":
    test_fusion_engine()
    test_weight_tuner()
