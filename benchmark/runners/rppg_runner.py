import os
import cv2
import json
import time
from .base_runner import BaseRunner
from inference.rppg_detector import RPPGDetector

class RPPGRunner(BaseRunner):
    def __init__(self, logger):
        super().__init__(logger)
        self.model = RPPGDetector()

    def run_frame(self, frame, metadata):
        start_time = time.time()
        try:
            score = self.model.update(frame)
        except Exception as e:
            score = 0.0
            
        latency = (time.time() - start_time) * 1000
        
        self.logger.log_prediction(
            frame_id=metadata.get("frame_id", "0"),
            video_id=metadata.get("video_id", "0"),
            subject_id=metadata.get("subject_id", "0"),
            dataset=metadata.get("dataset", "unknown"),
            ground_truth=metadata.get("ground_truth", "unknown"),
            prediction="live" if score > 0.5 else "spoof",
            confidence=score,
            component="rppg",
            latency_ms=latency
        )
        return score

    def run(self, dataset_path):
        self.logger.log_message(f"Starting rPPG benchmark on {dataset_path}")
        pass
