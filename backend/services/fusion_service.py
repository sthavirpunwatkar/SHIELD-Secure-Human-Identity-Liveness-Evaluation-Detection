import cv2
import numpy as np
import time
import sys
import os

# Add root to path to allow sibling imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from inference.face_detector import FaceDetector
from inference.liveness_classifier import LivenessClassifier
from inference.minifas_net import MiniFASNet
from inference.behavioral_analyzer import BehavioralAnalyzer
from inference.rppg_detector import RPPGDetector

class FusionService:
    def __init__(self):
        """
        Initializes all core AI models for orchestration.
        """
        self.detector = FaceDetector()
        self.primary_liveness = MiniFASNet() # MiniFASNet as primary
        self.secondary_liveness = LivenessClassifier() # EfficientNet as comparison
        self.behavioral = BehavioralAnalyzer()
        self.rppg = RPPGDetector()

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

        # 2. Multi-Modal Inference
        # Primary Liveness Score (MiniFASNet)
        p_verdict, p_conf = self.primary_liveness.predict(crop)
        p_score = p_conf if p_verdict == "Live" else (1.0 - p_conf)

        # Secondary Liveness Score (EfficientNet - Comparison)
        s_verdict, s_conf = self.secondary_liveness.predict(crop)
        s_score = s_conf if s_verdict == "Live" else (1.0 - s_conf)

        # Average Liveness for Fusion (or just use Primary)
        liveness_score = (p_score + s_score) / 2.0

        # Behavioral Score (Motion/Heuristics)
        behavior = self.behavioral.analyze(frame, faces=faces)
        # Simple behavioral score: 1.0 if landmarks found, bonus for blink
        behavioral_score = 0.7 if behavior['landmarks_found'] else 0.0
        if behavior['blink_detected']:
            behavioral_score = 1.0

        # Physiological Score (rPPG)
        rppg_score = self.rppg.update(frame)

        # 3. Decision Fusion (Weighted Average)
        # Weights: Liveness (40%), Behavioral (30%), rPPG (30%)
        weights = [0.4, 0.3, 0.3]
        scores = [liveness_score, behavioral_score, rppg_score]
        
        final_confidence = sum(s * w for s, w in zip(scores, weights))
        
        # 4. Final Verdict Logic
        if final_confidence > 0.65: # Lowered from 0.7
            verdict = "Live"
        elif final_confidence < 0.35: # Lowered from 0.4
            verdict = "Spoof"
        else:
            verdict = "Uncertain"

        processing_time = time.time() - start_time
        h, w = frame.shape[:2]

        return {
            "verdict": verdict,
            "confidence": round(final_confidence, 2),
            "status": "success",
            "processing_time_ms": int(processing_time * 1000),
            "frame_size": [w, h],
            "details": {
                "primary_liveness": round(p_score, 2),
                "secondary_liveness": round(s_score, 2),
                "combined_liveness": round(liveness_score, 2),
                "behavioral_score": round(behavioral_score, 2),
                "rppg_score": round(rppg_score, 2)
            },
            "bbox": bbox
        }

# Global instance
fusion_service = FusionService()
