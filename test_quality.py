import cv2
import numpy as np
from inference.quality import QualityScoreEngine

def test_quality_gate():
    print("--- SHIELD Face Quality Gate Test ---")
    engine = QualityScoreEngine()
    
    # 1. Test with a "good" quality dummy face
    # Create a neutral gray frame with a simulated "face" box
    frame = np.ones((480, 640, 3), dtype=np.uint8) * 100
    # Add a white rectangle for the face
    cv2.rectangle(frame, (200, 100), (400, 300), (200, 200, 200), -1)
    face_crop = frame[100:300, 200:400]
    
    # Add some noise to avoid zero variance in blur detector
    noise = np.random.normal(0, 5, face_crop.shape).astype(np.uint8)
    face_crop = cv2.add(face_crop, noise)
    
    print("\nTesting 'Good' Frame...")
    result = engine.evaluate(frame, face_crop)
    print(f"Quality Score: {result['quality_score']}")
    print(f"Passes Gate: {result['passes_gate']}")
    print(f"Blur Score: {result['metrics']['blur']['score']:.2f}")
    print(f"Illumination: {result['metrics']['illumination']['status']}")

    # 2. Test with a "blurry" frame
    blurry_face = cv2.GaussianBlur(face_crop, (21, 21), 0)
    print("\nTesting 'Blurry' Frame...")
    result = engine.evaluate(frame, blurry_face)
    print(f"Is Blurry: {result['metrics']['blur']['is_blurry']}")
    print(f"Passes Gate: {result['passes_gate']}")

    # 3. Test with "poor illumination" (Dark)
    dark_face = (face_crop * 0.1).astype(np.uint8)
    print("\nTesting 'Dark' Frame...")
    result = engine.evaluate(frame, dark_face)
    print(f"Illumination Status: {result['metrics']['illumination']['status']}")
    print(f"Passes Gate: {result['passes_gate']}")

    print("\n--- Quality Gate Test Complete ---")

if __name__ == "__main__":
    test_quality_gate()
