import os
import json
import cv2
import time
from inference.fusion_engine import FusionEngine
from inference.antispoof import AntispoofInference
from inference.rppg_detector import RPPGDetector
from inference.behavioral_analyzer import BehavioralAnalyzer
from .metrics import FASMetrics

class BenchmarkEngine:
    def __init__(self, manifest_path="data/processed/manifest.json"):
        self.manifest_path = manifest_path
        self.fusion_engine = FusionEngine()
        self.antispoof = AntispoofInference()
        self.rppg = RPPGDetector()
        self.behavioral = BehavioralAnalyzer()

    def run_benchmark(self):
        if not os.path.exists(self.manifest_path):
            print(f"Manifest not found at {self.manifest_path}. Run DataWrangler first.")
            return None

        with open(self.manifest_path, 'r') as f:
            manifest = json.load(f)

        print(f"--- Starting Benchmark on {len(manifest)} samples ---")
        
        results = []
        y_true = []
        y_pred = []
        
        start_time = time.time()
        
        for item in manifest:
            img_path = item["path"]
            label = item["label"]
            
            frame = cv2.imread(img_path)
            if frame is None: continue
            
            # Use simple center crop for benchmark if face detector is not explicitly called
            h, w = frame.shape[:2]
            crop = frame[int(h*0.2):int(h*0.8), int(w*0.2):int(w*0.8)]
            
            # Get component scores
            as_score = self.antispoof.predict(crop)
            rppg_score = self.rppg.update(frame)
            behavior = self.behavioral.analyze(frame)
            blink_score = 1.0 if behavior["blink_detected"] else 0.0
            
            # Fusion
            fusion_res = self.fusion_engine.fuse(
                rppg_score=rppg_score,
                blink_score=blink_score,
                antispoof_score=as_score,
                challenge_score=0.5 # Neutral placeholder
            )
            
            y_true.append(1 if label == "live" else 0)
            y_pred.append(fusion_res["final_score"])
            
            results.append({
                "path": img_path,
                "label": label,
                "score": fusion_res["final_score"],
                "verdict": fusion_res["verdict"]
            })

        total_time = time.time() - start_time
        fps = len(manifest) / total_time if total_time > 0 else 0
        
        metrics = FASMetrics.calculate(y_true, y_pred)
        metrics["fps"] = round(fps, 2)
        metrics["total_samples"] = len(manifest)
        
        return metrics, results

if __name__ == "__main__":
    engine = BenchmarkEngine()
    # stats, res = engine.run_benchmark()
    print("BenchmarkEngine ready.")
