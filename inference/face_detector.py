import cv2
import numpy as np
import os
from ultralytics import YOLO

class FaceDetector:
    def __init__(self, model_path='models/yolov8n-face.pt'):
        """
        Initializes the YOLOv8 face detector.
        :param model_path: Path to the YOLOv8-Face model weights.
        """
        # Search for models in models/ folder if not found
        if not os.path.exists(model_path) and not os.path.isabs(model_path):
            alt_path = os.path.join('models', os.path.basename(model_path))
            if os.path.exists(alt_path):
                model_path = alt_path

        try:
            self.model = YOLO(model_path)
        except Exception as e:
            print(f"Error loading model {model_path}: {e}")
            fallback = 'models/yolov8n.pt'
            print(f"Falling back to {fallback}")
            self.model = YOLO(fallback)

    def detect_faces(self, frame):
        """
        Detects faces in a given frame.
        :param frame: OpenCV image (BGR).
        :return: List of bounding boxes [x1, y1, x2, y2, confidence].
        """
        results = self.model(frame, verbose=False)
        faces = []
        
        for result in results:
            boxes = result.boxes
            for box in boxes:
                # Filter for person/face classes if using standard YOLO, 
                # or just take all if using YOLOv8-Face specific model
                # Class 0 in standard YOLO is 'person'
                cls = int(box.cls[0])
                conf = float(box.conf[0])
                
                # If we are using a specific face model, we don't need to filter by class 0
                # But for safety in this placeholder, we'll take boxes with conf > 0.35
                if conf > 0.35:
                    xyxy = box.xyxy[0].tolist()
                    faces.append({
                        'bbox': [int(x) for x in xyxy],
                        'confidence': conf
                    })
        
        return faces

    def crop_face(self, frame, bbox):
        """
        Crops a face from the frame based on a bounding box.
        :param frame: OpenCV image (BGR).
        :param bbox: [x1, y1, x2, y2].
        :return: Cropped image.
        """
        x1, y1, x2, y2 = bbox
        # Ensure coordinates are within frame boundaries
        h, w = frame.shape[:2]
        x1, y1 = max(0, x1), max(0, y1)
        x2, y2 = min(w, x2), min(h, y2)
        
        return frame[y1:y2, x1:x2]

if __name__ == "__main__":
    # Quick test logic
    detector = FaceDetector()
    print("FaceDetector initialized successfully.")
