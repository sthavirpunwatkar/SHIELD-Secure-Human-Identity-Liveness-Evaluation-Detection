import os
import json
import cv2
import time
import numpy as np
import sys

# Ensure root directory is in sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from inference.antispoof import AntispoofInference
from inference.rppg_detector import RPPGDetector
from inference.behavioral_analyzer import BehavioralAnalyzer
from evaluation.metrics import FASMetrics

class WeightTuner:
    def __init__(self, manifest_path):
        self.manifest_path = manifest_path
        self.antispoof = AntispoofInference()
        self.rppg = RPPGDetector()
        self.behavioral = BehavioralAnalyzer()

    def tune(self, min_weight=0.10):
        if not os.path.exists(self.manifest_path):
            print(f"Manifest not found at {self.manifest_path}.")
            return None

        with open(self.manifest_path, 'r') as f:
            manifest = json.load(f)

        print(f"Caching inference scores for {len(manifest)} samples...")
        samples_data = []
        
        for item in manifest:
            img_path = item["path"]
            label = item["label"]
            
            frame = cv2.imread(img_path)
            if frame is None:
                continue
            
            h, w = frame.shape[:2]
            crop = frame[int(h*0.2):int(h*0.8), int(w*0.2):int(w*0.8)]
            
            as_score = self.antispoof.predict(crop)
            rppg_score = self.rppg.update(frame)
            behavior = self.behavioral.analyze(frame)
            behavior_score = behavior.get("behavior_score", 0.0)
            challenge_score = 0.0  # Not testing active challenges here
            
            y_true = 1 if label == "live" else 0
            samples_data.append((y_true, rppg_score, behavior_score, as_score, challenge_score))

        print(f"Running grid search (min_weight={min_weight})...")
        best_acer = 1.0
        best_accuracy = 0.0
        best_weights = None
        
        # Grid search over 4 weights summing to 1.0
        for r_w in np.arange(min_weight, 1.01, 0.05):
            r_w = round(r_w, 2)
            for b_w in np.arange(min_weight, 1.01 - r_w, 0.05):
                b_w = round(b_w, 2)
                for a_w in np.arange(min_weight, 1.01 - r_w - b_w, 0.05):
                    a_w = round(a_w, 2)
                    c_w = round(1.0 - r_w - b_w - a_w, 2)
                    if c_w < round(min_weight, 2):
                        continue
                    
                    y_true_list = []
                    y_pred_scores = []
                    
                    for y_true, rppg_score, behavior_score, as_score, challenge_score in samples_data:
                        score = (r_w * rppg_score) + (b_w * behavior_score) + (a_w * as_score) + (c_w * challenge_score)
                        y_true_list.append(y_true)
                        y_pred_scores.append(score)
                        
                    metrics = FASMetrics.calculate(y_true_list, y_pred_scores)
                    acer = metrics["acer"]
                    accuracy = metrics["accuracy"]
                    
                    # Minimize ACER, use accuracy as tiebreaker
                    if acer < best_acer or (acer == best_acer and accuracy > best_accuracy):
                        best_acer = acer
                        best_accuracy = accuracy
                        best_weights = {
                            "rppg": r_w,
                            "behavior": b_w,
                            "antispoof": a_w,
                            "challenge": c_w
                        }

        return best_weights, best_acer, best_accuracy

if __name__ == "__main__":
    # Prioritize real processed manifest, fall back to processed_demo
    manifest = "data/processed/manifest.json"
    if not os.path.exists(manifest):
        manifest = "data/processed_demo/manifest.json"

    tuner = WeightTuner(manifest)
    result = tuner.tune(min_weight=0.10)
    if result:
        weights, acer, accuracy = result
        print("\n=== Optimal Fusion Weights Found ===")
        print(json.dumps(weights, indent=4))
        print(f"Best ACER: {acer * 100:.2f}%")
        print(f"Best Accuracy: {accuracy * 100:.2f}%")
