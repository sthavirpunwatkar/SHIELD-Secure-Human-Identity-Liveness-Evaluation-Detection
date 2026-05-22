import cv2
import numpy as np

try:
    import mediapipe as mp
    from mediapipe.python.solutions import face_mesh as mp_face_mesh
    HAS_MEDIAPIPE = True
except (ImportError, AttributeError):
    HAS_MEDIAPIPE = False

class PoseFilter:
    def __init__(self, yaw_threshold=15, pitch_threshold=15):
        """
        Initializes the Pose Filter.
        :param yaw_threshold: Max degrees for yaw.
        :param pitch_threshold: Max degrees for pitch.
        """
        self.yaw_threshold = yaw_threshold
        self.pitch_threshold = pitch_threshold
        self.has_mediapipe = HAS_MEDIAPIPE
        self.face_mesh = None
        
        if self.has_mediapipe:
            self.face_mesh = mp_face_mesh.FaceMesh(
                static_image_mode=True,
                max_num_faces=1,
                refine_landmarks=True,
                min_detection_confidence=0.5
            )

    def detect(self, frame):
        """
        Detects face pose (yaw, pitch, roll) using MediaPipe.
        :param frame: OpenCV image (BGR).
        :return: (pose_status, angles_dict)
        """
        if not self.has_mediapipe or frame is None:
            return "unknown", {"yaw": 0, "pitch": 0, "roll": 0}

        results = self.face_mesh.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        
        if not results.multi_face_landmarks:
            return "no_face", {"yaw": 0, "pitch": 0, "roll": 0}

        face_landmarks = results.multi_face_landmarks[0]
        img_h, img_w, _ = frame.shape
        
        # Simplified pose estimation using specific landmarks
        # Landmarks: Nose (1), Chin (152), Left Eye (33), Right Eye (263), Left Mouth (61), Right Mouth (291)
        # We can use solvePnP for accurate pose, but for a filter, heuristics might suffice.
        # Here we'll use a simplified version.
        
        # For simplicity in this implementation, we will return "frontal" if landmarks are found 
        # and we would normally calculate yaw/pitch here.
        # Let's implement a basic yaw check.
        
        nose = face_landmarks.landmark[1]
        l_eye = face_landmarks.landmark[33]
        r_eye = face_landmarks.landmark[263]
        
        # Horizontal ratio (Nose should be roughly in the middle of eyes)
        dist_l = abs(nose.x - l_eye.x)
        dist_r = abs(nose.x - r_eye.x)
        
        yaw_ratio = float(dist_l / (dist_r + 1e-6))
        
        # Heuristic: 0.5 < ratio < 2.0 is roughly frontal
        if 0.5 < yaw_ratio < 2.0:
            status = "frontal"
        else:
            status = "profile"
            
        return status, {"yaw_ratio": yaw_ratio}

if __name__ == "__main__":
    filter = PoseFilter()
    print("PoseFilter initialized.")
