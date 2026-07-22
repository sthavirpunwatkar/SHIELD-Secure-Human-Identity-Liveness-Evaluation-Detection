import numpy as np

class DummySession:
    def _get_landmark_coords(self, landmark):
        if hasattr(landmark, "x"):
            return np.array([landmark.x, landmark.y, landmark.z])
        elif isinstance(landmark, dict):
            return np.array([landmark.get("x", 0.0), landmark.get("y", 0.0), landmark.get("z", 0.0)])
        else:
            return np.array([landmark[0], landmark[1], landmark[2]])

    def _calculate_landmark_signature(self, landmarks):
        try:
            p_nose = self._get_landmark_coords(landmarks[1])
            p_leye = self._get_landmark_coords(landmarks[33])
            p_reye = self._get_landmark_coords(landmarks[263])
            p_chin = self._get_landmark_coords(landmarks[152])
            p_lmouth = self._get_landmark_coords(landmarks[61])
            p_rmouth = self._get_landmark_coords(landmarks[291])
            
            interocular = np.linalg.norm(p_leye - p_reye)
            if interocular == 0:
                print("Interocular is 0")
                return None
                
            d_nose_leye = np.linalg.norm(p_nose - p_leye) / interocular
            d_nose_reye = np.linalg.norm(p_nose - p_reye) / interocular
            d_mouth_width = np.linalg.norm(p_lmouth - p_rmouth) / interocular
            d_face_height = np.linalg.norm(p_nose - p_chin) / interocular
            
            return np.array([d_nose_leye, d_nose_reye, d_mouth_width, d_face_height])
        except Exception as e:
            print(f"Exception: {e}")
            return None

def make_mock_landmarks(nose, leye, reye, chin, lmouth, rmouth):
    l = [{"x": 0.0, "y": 0.0, "z": 0.0}] * 300
    l[1] = {"x": nose[0], "y": nose[1], "z": nose[2]}
    l[33] = {"x": leye[0], "y": leye[1], "z": leye[2]}
    l[263] = {"x": reye[0], "y": reye[1], "z": reye[2]}
    l[152] = {"x": chin[0], "y": chin[1], "z": chin[2]}
    l[61] = {"x": lmouth[0], "y": lmouth[1], "z": lmouth[2]}
    l[291] = {"x": rmouth[0], "y": rmouth[1], "z": rmouth[2]}
    return l

landmarks_1 = make_mock_landmarks(
    [0.0, 0.0, 0.0], [-0.1, 0.1, 0.0], [0.1, 0.1, 0.0],
    [0.0, -0.2, 0.0], [-0.05, -0.1, 0.0], [0.05, -0.1, 0.0]
)
landmarks_2 = make_mock_landmarks(
    [0.0, 0.0, 0.0], [-0.1, 0.1, 0.0], [0.1, 0.1, 0.0],
    [0.0, -0.6, 0.0], [-0.3, -0.1, 0.0], [0.3, -0.1, 0.0]
)

sess = DummySession()
sig1 = sess._calculate_landmark_signature(landmarks_1)
sig2 = sess._calculate_landmark_signature(landmarks_2)
print("Sig1:", sig1)
print("Sig2:", sig2)
if sig1 is not None and sig2 is not None:
    distance = np.linalg.norm(sig1 - sig2)
    print("Distance:", distance)
