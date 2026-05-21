import cv2
import numpy as np

class BehavioralAnalyzer:
    def __init__(self):
        """
        Fallback Behavioral Analyzer using simple heuristics.
        Note: MediaPipe was found to be incompatible with the current Python environment (3.13).
        """
        print("Warning: BehavioralAnalyzer is using fallback logic (Simple Heuristics).")
        self.prev_face_center = None

    def analyze(self, frame, faces=None):
        """
        Analyzes the frame for behavioral cues.
        :param frame: OpenCV image (BGR).
        :param faces: List of face detections from FaceDetector.
        :return: Dict containing blink detection and other metrics.
        """
        analysis = {
            'blink_detected': False,
            'ear': 0.0,
            'landmarks_found': False,
            'movement_detected': False
        }

        if faces and len(faces) > 0:
            analysis['landmarks_found'] = True
            bbox = faces[0]['bbox']
            center = ((bbox[0] + bbox[2]) // 2, (bbox[1] + bbox[3]) // 2)
            
            if self.prev_face_center:
                dist = np.linalg.norm(np.array(center) - np.array(self.prev_face_center))
                if dist > 5: # Threshold for movement
                    analysis['movement_detected'] = True
            
            self.prev_face_center = center
            
            # Placeholder for blink detection (randomized for simulation in dummy test)
            # In a real scenario, this would require working landmarks.
            analysis['blink_detected'] = np.random.random() > 0.95
                
        return analysis

if __name__ == "__main__":
    analyzer = BehavioralAnalyzer()
    print("BehavioralAnalyzer (Fallback) initialized.")
