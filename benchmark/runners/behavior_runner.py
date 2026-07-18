import os
import cv2
import json
import time
from .base_runner import BaseRunner
from inference.behavioral_analyzer import BehavioralAnalyzer

class BehaviorRunner(BaseRunner):
    def __init__(self, logger):
        super().__init__(logger)
        self.model = BehavioralAnalyzer()

    def run_frame(self, frame, metadata):
        start_time = time.time()
        
        result = self.model.analyze(frame)
        
        latency = (time.time() - start_time) * 1000
        
        # Behavior doesn't strictly output live/spoof confidence in the same way, 
        # it outputs blink_detected and pose.
        score = 1.0 if result.get("blink_detected", False) else 0.0
        
        self.logger.log_prediction(
            frame_id=metadata.get("frame_id", "0"),
            video_id=metadata.get("video_id", "0"),
            subject_id=metadata.get("subject_id", "0"),
            dataset=metadata.get("dataset", "unknown"),
            ground_truth=metadata.get("ground_truth", "unknown"),
            prediction="live" if score > 0.5 else "spoof",
            confidence=score,
            component="behavior",
            latency_ms=latency
        )
        return result

    def run(self, dataset_path):
        self.logger.log_message(f"Starting Behavior benchmark on {dataset_path}")
        pass
