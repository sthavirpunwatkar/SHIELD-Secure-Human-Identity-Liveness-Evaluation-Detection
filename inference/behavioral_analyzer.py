import cv2
import numpy as np
import math

try:
    import mediapipe as mp
    from mediapipe.python.solutions import face_mesh as mp_face_mesh
    HAS_MEDIAPIPE = True
    USE_TASKS_API = False
except (ImportError, AttributeError):
    try:
        import mediapipe.solutions.face_mesh as mp_face_mesh
        HAS_MEDIAPIPE = True
        USE_TASKS_API = False
    except (ImportError, AttributeError):
        try:
            from mediapipe.tasks import python
            from mediapipe.tasks.python import vision
            HAS_MEDIAPIPE = True
            USE_TASKS_API = True
        except ImportError:
            HAS_MEDIAPIPE = False
            USE_TASKS_API = False


# ============================================================
# MediaPipe Face Mesh 468-point Landmark Indices
# ============================================================

# Left eye contour landmarks (for EAR calculation)
LEFT_EYE_LANDMARKS = {
    "outer": 33,    # Left eye outer corner
    "inner": 133,   # Left eye inner corner
    "upper_1": 160, # Upper eyelid point 1
    "upper_2": 158, # Upper eyelid point 2
    "lower_1": 153, # Lower eyelid point 1
    "lower_2": 144, # Lower eyelid point 2
}

# Right eye contour landmarks (for EAR calculation)
RIGHT_EYE_LANDMARKS = {
    "outer": 362,   # Right eye outer corner
    "inner": 263,   # Right eye inner corner
    "upper_1": 385, # Upper eyelid point 1
    "upper_2": 387, # Upper eyelid point 2
    "lower_1": 373, # Lower eyelid point 1
    "lower_2": 380, # Lower eyelid point 2
}

# Mouth landmarks (for MAR / smile detection)
MOUTH_LANDMARKS = {
    "left_corner": 61,    # Left lip corner
    "right_corner": 291,  # Right lip corner
    "upper_lip": 13,      # Upper lip center
    "lower_lip": 14,      # Lower lip center
    "upper_outer": 0,     # Upper lip outer (for smile)
    "lower_outer": 17,    # Lower lip outer / chin ref
}

# Head pose estimation landmarks (6-point model for solvePnP)
POSE_LANDMARKS = {
    "nose_tip": 1,
    "chin": 152,
    "left_eye_corner": 33,
    "right_eye_corner": 263,
    "left_mouth_corner": 61,
    "right_mouth_corner": 291,
}

# 3D model points for solvePnP (generic face model in mm)
MODEL_POINTS_3D = np.array([
    (0.0, 0.0, 0.0),            # Nose tip
    (0.0, -330.0, -65.0),       # Chin
    (-225.0, 170.0, -135.0),    # Left eye left corner
    (225.0, 170.0, -135.0),     # Right eye right corner
    (-150.0, -150.0, -125.0),   # Left mouth corner
    (150.0, -150.0, -125.0),    # Right mouth corner
], dtype=np.float64)


class BehavioralAnalyzer:
    # ============================================================
    # Configurable thresholds
    # ============================================================
    EAR_BLINK_THRESHOLD = 0.21       # Below this = eye is closed / blink
    MAR_MOUTH_OPEN_THRESHOLD = 0.6   # Above this = mouth is open
    SMILE_RATIO_THRESHOLD = 1.8      # Corner distance / vertical > this = smile
    YAW_TURN_THRESHOLD = 15.0        # Degrees; > this = head turned
    PITCH_NOD_THRESHOLD = 10.0       # Degrees; > this = head nodding

    def __init__(self):
        """
        Initializes Behavioral analysis. Falls back to simple heuristics if MediaPipe fails.

        Implements:
        - EAR (Eye Aspect Ratio) for blink detection
        - MAR (Mouth Aspect Ratio) for mouth-open detection
        - Smile ratio from lip corner geometry
        - solvePnP-based head pose estimation (yaw, pitch, roll)
        - Unified challenge verification dispatcher
        """
        self.has_mediapipe = HAS_MEDIAPIPE
        self.face_mesh = None
        self.landmarker = None
        self.use_tasks_api = USE_TASKS_API

        # Temporal tracking for blink detection
        self._prev_ear = None
        self._blink_counter = 0
        self._ear_history = []       # Last N EAR values for smoothing
        self._ear_window_size = 5

        if self.has_mediapipe:
            if not self.use_tasks_api:
                try:
                    self.face_mesh = mp_face_mesh.FaceMesh(
                        static_image_mode=False,
                        max_num_faces=1,
                        refine_landmarks=True,
                        min_detection_confidence=0.5,
                        min_tracking_confidence=0.5
                    )
                    print("BehavioralAnalyzer: MediaPipe FaceMesh initialized.")
                except Exception as e:
                    print(f"BehavioralAnalyzer: MediaPipe init failed: {e}. Using fallback.")
                    self.has_mediapipe = False
            else:
                try:
                    base_options = python.BaseOptions(model_asset_path='models/face_landmarker.task')
                    options = vision.FaceLandmarkerOptions(
                        base_options=base_options,
                        output_face_blendshapes=False,
                        output_facial_transformation_matrixes=False,
                        num_faces=1
                    )
                    self.landmarker = vision.FaceLandmarker.create_from_options(options)
                    print("BehavioralAnalyzer: MediaPipe FaceLandmarker (Tasks API) initialized.")
                except Exception as e:
                    print(f"BehavioralAnalyzer: Tasks FaceLandmarker init failed: {e}. Using fallback.")
                    self.has_mediapipe = False
        else:
            print("BehavioralAnalyzer: MediaPipe not available. Using fallback logic.")

    # ============================================================
    # Core Geometry Helpers
    # ============================================================

    @staticmethod
    def _landmark_to_point(landmark, img_w, img_h):
        """Convert a normalized MediaPipe landmark to pixel coordinates."""
        return np.array([landmark.x * img_w, landmark.y * img_h])

    @staticmethod
    def _landmark_to_point_3(landmark, img_w, img_h):
        """Convert a normalized MediaPipe landmark to pixel coordinates (2D for solvePnP)."""
        return (landmark.x * img_w, landmark.y * img_h)

    @staticmethod
    def _euclidean_distance(p1, p2):
        """Euclidean distance between two 2D points."""
        return np.linalg.norm(p1 - p2)

    # ============================================================
    # EAR — Eye Aspect Ratio
    # ============================================================

    def _compute_ear(self, landmarks, img_w, img_h, eye_indices):
        """
        Computes the Eye Aspect Ratio (EAR) for a single eye.

        EAR = (||p2 - p6|| + ||p3 - p5||) / (2 * ||p1 - p4||)

        Where p1=outer, p2=upper_1, p3=upper_2, p4=inner, p5=lower_2, p6=lower_1

        :param landmarks: MediaPipe face landmarks.
        :param img_w: Image width in pixels.
        :param img_h: Image height in pixels.
        :param eye_indices: Dict with keys outer, inner, upper_1, upper_2, lower_1, lower_2.
        :return: EAR value (float). Lower = more closed.
        """
        p_outer = self._landmark_to_point(landmarks[eye_indices["outer"]], img_w, img_h)
        p_inner = self._landmark_to_point(landmarks[eye_indices["inner"]], img_w, img_h)
        p_upper_1 = self._landmark_to_point(landmarks[eye_indices["upper_1"]], img_w, img_h)
        p_upper_2 = self._landmark_to_point(landmarks[eye_indices["upper_2"]], img_w, img_h)
        p_lower_1 = self._landmark_to_point(landmarks[eye_indices["lower_1"]], img_w, img_h)
        p_lower_2 = self._landmark_to_point(landmarks[eye_indices["lower_2"]], img_w, img_h)

        # Vertical distances
        v1 = self._euclidean_distance(p_upper_1, p_lower_1)
        v2 = self._euclidean_distance(p_upper_2, p_lower_2)

        # Horizontal distance
        h = self._euclidean_distance(p_outer, p_inner)

        if h == 0:
            return 0.3  # Fallback to "open" if detection fails

        ear = (v1 + v2) / (2.0 * h)
        return ear

    def detect_blink(self, landmarks, img_w, img_h):
        """
        Detects if a blink is occurring using EAR on both eyes.

        A blink is detected when the average EAR drops below the threshold
        AND was previously above it (transition detection).

        :param landmarks: MediaPipe face landmarks list.
        :param img_w: Image width.
        :param img_h: Image height.
        :return: (blink_detected: bool, avg_ear: float)
        """
        left_ear = self._compute_ear(landmarks, img_w, img_h, LEFT_EYE_LANDMARKS)
        right_ear = self._compute_ear(landmarks, img_w, img_h, RIGHT_EYE_LANDMARKS)
        avg_ear = (left_ear + right_ear) / 2.0

        # Update EAR history for smoothing
        self._ear_history.append(avg_ear)
        if len(self._ear_history) > self._ear_window_size:
            self._ear_history.pop(0)

        # Detect blink: EAR drops below threshold (transition from open to closed)
        blink_detected = False
        if self._prev_ear is not None:
            if self._prev_ear >= self.EAR_BLINK_THRESHOLD and avg_ear < self.EAR_BLINK_THRESHOLD:
                blink_detected = True
                self._blink_counter += 1

        self._prev_ear = avg_ear
        return blink_detected, avg_ear

    # ============================================================
    # MAR — Mouth Aspect Ratio / Smile Detection
    # ============================================================

    def detect_mouth_open(self, landmarks, img_w, img_h):
        """
        Detects if the mouth is open using MAR (Mouth Aspect Ratio).

        MAR = vertical_distance / horizontal_distance

        :param landmarks: MediaPipe face landmarks list.
        :param img_w: Image width.
        :param img_h: Image height.
        :return: (is_open: bool, mar: float)
        """
        upper_lip = self._landmark_to_point(landmarks[MOUTH_LANDMARKS["upper_lip"]], img_w, img_h)
        lower_lip = self._landmark_to_point(landmarks[MOUTH_LANDMARKS["lower_lip"]], img_w, img_h)
        left_corner = self._landmark_to_point(landmarks[MOUTH_LANDMARKS["left_corner"]], img_w, img_h)
        right_corner = self._landmark_to_point(landmarks[MOUTH_LANDMARKS["right_corner"]], img_w, img_h)

        vertical = self._euclidean_distance(upper_lip, lower_lip)
        horizontal = self._euclidean_distance(left_corner, right_corner)

        if horizontal == 0:
            return False, 0.0

        mar = vertical / horizontal
        is_open = mar > self.MAR_MOUTH_OPEN_THRESHOLD
        return is_open, mar

    def detect_smile(self, landmarks, img_w, img_h):
        """
        Detects a smile using the ratio of lip corner distance to vertical mouth opening.

        When smiling, corners spread wide while vertical opening stays small,
        resulting in a high corner_distance / vertical_distance ratio.

        :param landmarks: MediaPipe face landmarks list.
        :param img_w: Image width.
        :param img_h: Image height.
        :return: (is_smiling: bool, smile_ratio: float)
        """
        upper_lip = self._landmark_to_point(landmarks[MOUTH_LANDMARKS["upper_lip"]], img_w, img_h)
        lower_lip = self._landmark_to_point(landmarks[MOUTH_LANDMARKS["lower_lip"]], img_w, img_h)
        left_corner = self._landmark_to_point(landmarks[MOUTH_LANDMARKS["left_corner"]], img_w, img_h)
        right_corner = self._landmark_to_point(landmarks[MOUTH_LANDMARKS["right_corner"]], img_w, img_h)

        corner_distance = self._euclidean_distance(left_corner, right_corner)
        vertical_distance = self._euclidean_distance(upper_lip, lower_lip)

        if vertical_distance == 0:
            # Mouth is fully closed — check corner distance against face width heuristic
            smile_ratio = corner_distance / 1.0  # Avoid div by zero
            return False, smile_ratio

        smile_ratio = corner_distance / vertical_distance
        is_smiling = smile_ratio > self.SMILE_RATIO_THRESHOLD
        return is_smiling, smile_ratio

    # ============================================================
    # Head Pose Estimation (solvePnP)
    # ============================================================

    def estimate_head_pose(self, landmarks, img_w, img_h):
        """
        Estimates head pose (yaw, pitch, roll) using cv2.solvePnP with 6 facial landmarks.

        Uses a generic 3D face model and projects it against the 2D landmarks
        to compute the rotation vector, which is then converted to Euler angles.

        :param landmarks: MediaPipe face landmarks list.
        :param img_w: Image width.
        :param img_h: Image height.
        :return: dict with 'yaw', 'pitch', 'roll' in degrees.
        """
        # Extract 2D image points
        image_points = np.array([
            self._landmark_to_point_3(landmarks[POSE_LANDMARKS["nose_tip"]], img_w, img_h),
            self._landmark_to_point_3(landmarks[POSE_LANDMARKS["chin"]], img_w, img_h),
            self._landmark_to_point_3(landmarks[POSE_LANDMARKS["left_eye_corner"]], img_w, img_h),
            self._landmark_to_point_3(landmarks[POSE_LANDMARKS["right_eye_corner"]], img_w, img_h),
            self._landmark_to_point_3(landmarks[POSE_LANDMARKS["left_mouth_corner"]], img_w, img_h),
            self._landmark_to_point_3(landmarks[POSE_LANDMARKS["right_mouth_corner"]], img_w, img_h),
        ], dtype=np.float64)

        # Camera intrinsics (approximate using image dimensions)
        focal_length = img_w
        center = (img_w / 2.0, img_h / 2.0)
        camera_matrix = np.array([
            [focal_length, 0, center[0]],
            [0, focal_length, center[1]],
            [0, 0, 1]
        ], dtype=np.float64)

        dist_coeffs = np.zeros((4, 1))  # Assume no lens distortion

        # Solve PnP
        success, rotation_vector, translation_vector = cv2.solvePnP(
            MODEL_POINTS_3D, image_points, camera_matrix, dist_coeffs,
            flags=cv2.SOLVEPNP_ITERATIVE
        )

        if not success:
            return {"yaw": 0.0, "pitch": 0.0, "roll": 0.0}

        # Convert rotation vector to rotation matrix, then to Euler angles
        rotation_matrix, _ = cv2.Rodrigues(rotation_vector)
        pose_matrix = cv2.hconcat([rotation_matrix, translation_vector])
        _, _, _, _, _, _, euler_angles = cv2.decomposeProjectionMatrix(
            cv2.hconcat([pose_matrix, np.array([[0, 0, 0, 1]], dtype=np.float64)])
        )

        # euler_angles are in (pitch, yaw, roll) order from decomposeProjectionMatrix
        pitch = float(euler_angles[0][0])
        yaw = float(euler_angles[1][0])
        roll = float(euler_angles[2][0])

        return {"yaw": yaw, "pitch": pitch, "roll": roll}

    # ============================================================
    # Challenge Verification Dispatcher
    # ============================================================

    def verify_challenge(self, frame, challenge_type):
        """
        Verifies whether the user is performing the specified challenge action.

        :param frame: OpenCV image (BGR).
        :param challenge_type: String — one of 'blink', 'turn_left', 'turn_right',
                               'nod_up', 'nod_down', 'smile', 'open_mouth'.
        :return: dict with 'action_detected' (bool), 'confidence' (float), 'details' (dict).
        """
        result = {
            "action_detected": False,
            "confidence": 0.0,
            "details": {},
            "landmarks_found": False
        }

        if not self.has_mediapipe or (not self.face_mesh and not self.landmarker):
            return result

        try:
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            face_landmarks = None
            
            if not self.use_tasks_api and self.face_mesh:
                processed = self.face_mesh.process(rgb_frame)
                if processed.multi_face_landmarks:
                    face_landmarks = processed.multi_face_landmarks[0].landmark
            elif self.use_tasks_api and self.landmarker:
                import mediapipe as mp
                mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)
                processed = self.landmarker.detect(mp_image)
                if processed.face_landmarks:
                    face_landmarks = processed.face_landmarks[0]
                    
            if face_landmarks is None:
                return result

            result["landmarks_found"] = True
            img_h, img_w = frame.shape[:2]

            if challenge_type == "blink":
                blink_detected, ear = self.detect_blink(face_landmarks, img_w, img_h)
                result["action_detected"] = blink_detected
                result["confidence"] = 1.0 - (ear / self.EAR_BLINK_THRESHOLD) if ear < self.EAR_BLINK_THRESHOLD else 0.0
                result["details"] = {"ear": round(ear, 4), "threshold": self.EAR_BLINK_THRESHOLD}

            elif challenge_type == "smile":
                is_smiling, smile_ratio = self.detect_smile(face_landmarks, img_w, img_h)
                result["action_detected"] = is_smiling
                result["confidence"] = min(1.0, smile_ratio / self.SMILE_RATIO_THRESHOLD) if is_smiling else 0.0
                result["details"] = {"smile_ratio": round(smile_ratio, 4), "threshold": self.SMILE_RATIO_THRESHOLD}

            elif challenge_type == "open_mouth":
                is_open, mar = self.detect_mouth_open(face_landmarks, img_w, img_h)
                result["action_detected"] = is_open
                result["confidence"] = min(1.0, mar / self.MAR_MOUTH_OPEN_THRESHOLD) if is_open else 0.0
                result["details"] = {"mar": round(mar, 4), "threshold": self.MAR_MOUTH_OPEN_THRESHOLD}

            elif challenge_type in ("turn_left", "turn_right", "nod_up", "nod_down"):
                pose = self.estimate_head_pose(face_landmarks, img_w, img_h)
                result["details"] = {
                    "yaw": round(pose["yaw"], 2),
                    "pitch": round(pose["pitch"], 2),
                    "roll": round(pose["roll"], 2)
                }

                if challenge_type == "turn_left":
                    result["action_detected"] = pose["yaw"] < -self.YAW_TURN_THRESHOLD
                    result["confidence"] = min(1.0, abs(pose["yaw"]) / (self.YAW_TURN_THRESHOLD * 2))
                elif challenge_type == "turn_right":
                    result["action_detected"] = pose["yaw"] > self.YAW_TURN_THRESHOLD
                    result["confidence"] = min(1.0, abs(pose["yaw"]) / (self.YAW_TURN_THRESHOLD * 2))
                elif challenge_type == "nod_up":
                    result["action_detected"] = pose["pitch"] < -self.PITCH_NOD_THRESHOLD
                    result["confidence"] = min(1.0, abs(pose["pitch"]) / (self.PITCH_NOD_THRESHOLD * 2))
                elif challenge_type == "nod_down":
                    result["action_detected"] = pose["pitch"] > self.PITCH_NOD_THRESHOLD
                    result["confidence"] = min(1.0, abs(pose["pitch"]) / (self.PITCH_NOD_THRESHOLD * 2))

            return result

        except Exception as e:
            print(f"BehavioralAnalyzer: verify_challenge error: {e}")
            return result

    # ============================================================
    # Legacy Interface (Backward Compatible)
    # ============================================================

    def analyze(self, frame, faces=None):
        """
        Analyzes motion, blinks, and head turns.
        Backward-compatible with the original interface.

        Now uses real EAR-based blink detection and solvePnP head pose
        instead of placeholder logic.
        """
        results = {
            "blink_detected": False,
            "head_turn": "center",
            "landmarks_found": False,
            "ear": 0.0,
            "pose": {"yaw": 0.0, "pitch": 0.0, "roll": 0.0},
            "blink_count": self._blink_counter
        }

        if self.has_mediapipe and (self.face_mesh or self.landmarker):
            try:
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                face_landmarks = None
                
                if not self.use_tasks_api and self.face_mesh:
                    processed = self.face_mesh.process(rgb_frame)
                    if processed.multi_face_landmarks:
                        face_landmarks = processed.multi_face_landmarks[0].landmark
                elif self.use_tasks_api and self.landmarker:
                    import mediapipe as mp
                    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)
                    processed = self.landmarker.detect(mp_image)
                    if processed.face_landmarks:
                        face_landmarks = processed.face_landmarks[0]
                        
                if face_landmarks is not None:
                    results["landmarks_found"] = True
                    img_h, img_w = frame.shape[:2]

                    # Real EAR-based blink detection
                    blink_detected, avg_ear = self.detect_blink(face_landmarks, img_w, img_h)
                    results["blink_detected"] = blink_detected
                    results["ear"] = round(avg_ear, 4)
                    results["blink_count"] = self._blink_counter

                    # Real solvePnP head pose estimation
                    pose = self.estimate_head_pose(face_landmarks, img_w, img_h)
                    results["pose"] = pose

                    # Classify head turn direction
                    yaw = pose["yaw"]
                    if yaw < -self.YAW_TURN_THRESHOLD:
                        results["head_turn"] = "left"
                    elif yaw > self.YAW_TURN_THRESHOLD:
                        results["head_turn"] = "right"
                    else:
                        results["head_turn"] = "center"

                    return results
            except Exception as e:
                print(f"BehavioralAnalyzer: MediaPipe processing error: {e}")

        # Fallback Logic (if MediaPipe is missing or fails)
        if faces and len(faces) > 0:
            results["landmarks_found"] = True
            bbox = faces[0]['bbox']
            # Simple heuristic: If face is large enough, assume some behavioral presence
            if (bbox[2] - bbox[0]) > 80:
                results["blink_detected"] = True

        return results

    def reset_counters(self):
        """Resets temporal tracking counters (call between sessions)."""
        self._prev_ear = None
        self._blink_counter = 0
        self._ear_history = []


if __name__ == "__main__":
    analyzer = BehavioralAnalyzer()
    print("BehavioralAnalyzer ready.")
    print(f"  MediaPipe available: {analyzer.has_mediapipe}")
    print(f"  EAR threshold: {analyzer.EAR_BLINK_THRESHOLD}")
    print(f"  MAR threshold: {analyzer.MAR_MOUTH_OPEN_THRESHOLD}")
    print(f"  Smile ratio threshold: {analyzer.SMILE_RATIO_THRESHOLD}")
    print(f"  Yaw turn threshold: {analyzer.YAW_TURN_THRESHOLD}°")
    print(f"  Pitch nod threshold: {analyzer.PITCH_NOD_THRESHOLD}°")
