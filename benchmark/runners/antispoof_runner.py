import os
import cv2
import json
import time
from .base_runner import BaseRunner
from inference.antispoof.inference import AntispoofInference

class AntiSpoofRunner(BaseRunner):
    def __init__(self, logger):
        super().__init__(logger)
        self.model = AntispoofInference()
        # Ensure we log the checksum of the loaded model
        self.logger.record_model_checksums([self.model.model_path])

    def run_frame(self, frame, metadata):
        """
        Runs inference on a single frame for parity testing.
        """
        start_time = time.time()
        
        # In a real benchmark, we might run face detection here first.
        # For this runner, we assume the frame is already the face crop or we do detection inside.
        # production AntispoofInference.predict expects a face crop.
        try:
            score = self.model.predict(frame)
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
            component="antispoof",
            latency_ms=latency
        )
        return score

    def get_intermediate_tensors(self, frame):
        """
        Helper for parity testing. 
        """
        # We need to simulate the preprocessing to compare it.
        # production preprocessing is done inside `predict()` via `preprocess()`.
        processed = self.model.preprocess(frame)
        # return the tensor for comparison
        return processed

    def run(self, dataset_path):
        self.logger.log_message(f"Starting AntiSpoof benchmark on {dataset_path}")
        # In a real scenario, we walk the dataset and call run_frame.
        pass
