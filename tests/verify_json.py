import json
import numpy as np
import cv2
from inference.quality import QualityScoreEngine

def verify_serialization():
    print("--- Verifying JSON Serialization of Quality Metrics ---")
    engine = QualityScoreEngine()
    
    # Create a dummy frame
    frame = np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)
    face_crop = frame[100:300, 200:400]
    
    result = engine.evaluate(frame, face_crop)
    
    try:
        json_str = json.dumps(result, indent=4)
        print("Success: Result is JSON serializable.")
        print(json_str)
    except TypeError as e:
        print(f"Error: Result is NOT JSON serializable. {e}")
        # Identify the non-serializable type
        for key, value in result.items():
            print(f"{key}: {type(value)}")
            if isinstance(value, dict):
                for k, v in value.items():
                    print(f"  {k}: {type(v)}")

if __name__ == "__main__":
    verify_serialization()
