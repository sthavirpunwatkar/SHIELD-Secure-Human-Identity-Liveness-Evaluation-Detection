import cv2
import numpy as np
from inference.face_detector import FaceDetector
from inference.antispoof import AntispoofInference
from inference.behavioral_analyzer import BehavioralAnalyzer
from inference.rppg_detector import RPPGDetector

def main():
    print("--- SHIELD Inference Pipeline Test ---")
    
    # Initialize models
    detector = FaceDetector()
    antispoof = AntispoofInference()
    behavioral = BehavioralAnalyzer()
    rppg = RPPGDetector()
    
    # Create a dummy frame (640x480 black image)
    frame = np.zeros((480, 640, 3), dtype=np.uint8)
    # Add a white rectangle to simulate a face
    cv2.rectangle(frame, (200, 100), (400, 300), (255, 255, 255), -1)
    
    print("1. Testing Face Detection...")
    faces = detector.detect_faces(frame)
    
    # Force a face if detection fails for testing purposes
    if not faces:
        print("No faces detected in dummy frame. Forcing a test face...")
        faces = [{'bbox': [200, 100, 400, 300], 'confidence': 1.0}]
    
    print(f"Processing {len(faces)} face(s).")
    
    if faces:
        face_info = faces[0]
        bbox = face_info['bbox']
        crop = detector.crop_face(frame, bbox)
        
        print("2. Testing Behavioral Analysis...")
        behavior = behavioral.analyze(frame, faces=faces)
        print(f"Blink Detected: {behavior['blink_detected']}, Landmarks Found: {behavior['landmarks_found']}")
        
        print("3. Testing Antispoof Classification...")
        as_score = antispoof.predict(crop)
        print(f"Antispoof Score (Real=1.0): {as_score:.2f}")
        
        print("4. Testing rPPG Analysis...")
        rppg_score = rppg.update(frame)
        print(f"rPPG Liveness Score: {rppg_score:.2f}")
        
    print("\n--- Pipeline Verification Complete ---")

if __name__ == "__main__":
    main()
