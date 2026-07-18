import os
import cv2
import json
import time
from .base_runner import BaseRunner
from inference.fusion_engine import FusionEngine

class FusionRunner(BaseRunner):
    def __init__(self, logger):
        super().__init__(logger)
        self.model = FusionEngine()

    def run_fusion(self, rppg_score, blink_score, antispoof_score, challenge_score, is_challenge_active, metadata):
        start_time = time.time()
        
        result = self.model.fuse(rppg_score, blink_score, antispoof_score, challenge_score, is_challenge_active)
        
        latency = (time.time() - start_time) * 1000
        
        score = result["final_score"]
        
        self.logger.log_prediction(
            frame_id=metadata.get("frame_id", "0"),
            video_id=metadata.get("video_id", "0"),
            subject_id=metadata.get("subject_id", "0"),
            dataset=metadata.get("dataset", "unknown"),
            ground_truth=metadata.get("ground_truth", "unknown"),
            prediction="live" if result["verdict"] == "Live" else "spoof",
            confidence=score,
            component="fusion",
            latency_ms=latency
        )
        return result

    def run(self, dataset_path):
        self.logger.log_message(f"Starting complete Fusion pipeline benchmark on {dataset_path}")
        pass
