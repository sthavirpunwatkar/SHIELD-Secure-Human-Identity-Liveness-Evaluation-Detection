import cv2
import numpy as np
import time
import sys
import os

# Add root to path to allow sibling imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from inference.face_detector import FaceDetector
from inference.liveness_classifier import LivenessClassifier
from inference.antispoof import AntispoofInference
from inference.behavioral_analyzer import BehavioralAnalyzer
from inference.rppg_detector import RPPGDetector
from inference.quality import QualityScoreEngine
from inference.fusion_engine import FusionEngine

class FusionService:
    def __init__(self):
        """
        Initializes all core AI models for orchestration.
        """
        self.detector = FaceDetector()
        self.quality_engine = QualityScoreEngine()
        self.antispoof = AntispoofInference()
        self.secondary_liveness = LivenessClassifier()
        self.behavioral = BehavioralAnalyzer()
        self.rppg = RPPGDetector()
        self.fusion_engine = FusionEngine()

    def process_frame(self, frame):
        """
        Runs the multi-modal pipeline on a single frame.
        :param frame: OpenCV image (BGR).
        :return: Dict containing the final verdict and detailed scores.
        """
        start_time = time.time()
        
        # 1. Face Detection
        faces = self.detector.detect_faces(frame)
        if not faces:
            return {
                "verdict": "No Face Detected",
                "confidence": 0.0,
                "status": "fail",
                "details": {}
            }

        face_info = faces[0]
        bbox = face_info['bbox']
        crop = self.detector.crop_face(frame, bbox)

        # 2. Quality Gate
        quality_res = self.quality_engine.evaluate(frame, crop)
        if not quality_res["passes_gate"]:
            return {
                "verdict": "Low Quality",
                "confidence": quality_res["quality_score"],
                "status": "fail",
                "quality_metrics": quality_res["metrics"],
                "details": {"reason": "Quality gate failed"}
            }

        # 3. Multi-Modal Inference
        as_score = self.antispoof.predict(crop)
        
        # Behavioral Score (Blink)
        behavior = self.behavioral.analyze(frame, faces=faces)
        blink_score = 1.0 if behavior['blink_detected'] else 0.0

        # Physiological Score (rPPG)
        rppg_score = self.rppg.update(frame)

        # 4. Decision Fusion
        fusion_res = self.fusion_engine.fuse(
            rppg_score=rppg_score,
            blink_score=blink_score,
            antispoof_score=as_score,
            challenge_score=0.5
        )

        processing_time = time.time() - start_time
        h, w = frame.shape[:2]

        return {
            "verdict": fusion_res["verdict"],
            "confidence": fusion_res["final_score"],
            "status": "success",
            "processing_time_ms": int(processing_time * 1000),
            "frame_size": [w, h],
            "details": fusion_res["breakdown"],
            "quality_metrics": quality_res["metrics"],
            "bbox": bbox
        }

# Global instance
fusion_service = FusionService()
