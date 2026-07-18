import os
import sys
import json
import time
import platform
import subprocess
import hashlib
from datetime import datetime

class BenchmarkLogger:
    def __init__(self, run_name="experiment"):
        self.timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        self.output_dir = os.path.join("benchmark", "outputs", f"{self.timestamp}_{run_name}")
        os.makedirs(self.output_dir, exist_ok=True)
        
        self.predictions_path = os.path.join(self.output_dir, "predictions.jsonl")
        self.log_path = os.path.join(self.output_dir, "benchmark.log")
        
        self._record_system_info()
        self._record_git_commit()
        
    def _record_system_info(self):
        sys_info = {
            "os": platform.system(),
            "os_release": platform.release(),
            "python_version": platform.python_version(),
            "cpu": platform.processor(),
            "timestamp": self.timestamp
        }
        
        try:
            import onnxruntime as ort
            sys_info["onnxruntime_version"] = ort.__version__
            sys_info["onnx_device"] = ort.get_device()
        except ImportError:
            sys_info["onnxruntime_version"] = "Not Installed"
            
        with open(os.path.join(self.output_dir, "system_info.json"), "w") as f:
            json.dump(sys_info, f, indent=4)
            
    def _record_git_commit(self):
        try:
            commit = subprocess.check_output(["git", "rev-parse", "HEAD"]).decode("utf-8").strip()
        except Exception:
            commit = "Unknown"
            
        with open(os.path.join(self.output_dir, "git_commit.txt"), "w") as f:
            f.write(f"Commit: {commit}\n")

    def record_model_checksums(self, model_paths):
        checksums = {}
        for path in model_paths:
            if os.path.exists(path):
                with open(path, "rb") as f:
                    checksums[path] = hashlib.sha256(f.read()).hexdigest()
            else:
                checksums[path] = "FILE_NOT_FOUND"
                
        with open(os.path.join(self.output_dir, "model_checksums.json"), "w") as f:
            json.dump(checksums, f, indent=4)
            
    def log_prediction(self, frame_id, video_id, subject_id, dataset, ground_truth, prediction, confidence, component, latency_ms):
        record = {
            "frame_id": str(frame_id),
            "video_id": str(video_id),
            "subject_id": str(subject_id),
            "dataset": str(dataset),
            "ground_truth": str(ground_truth),
            "prediction": str(prediction),
            "confidence": float(confidence),
            "component": str(component),
            "latency_ms": float(latency_ms)
        }
        with open(self.predictions_path, "a") as f:
            f.write(json.dumps(record) + "\n")
            
    def log_message(self, message):
        msg = f"[{datetime.now().isoformat()}] {message}\n"
        print(msg.strip())
        with open(self.log_path, "a") as f:
            f.write(msg)
            
    def save_metrics(self, metrics_dict):
        with open(os.path.join(self.output_dir, "metrics.json"), "w") as f:
            json.dump(metrics_dict, f, indent=4)
