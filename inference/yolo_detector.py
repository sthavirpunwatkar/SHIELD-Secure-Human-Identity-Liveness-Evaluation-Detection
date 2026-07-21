import cv2
import numpy as np
import os
from ultralytics import YOLO

class YoloSegDetector:
    def __init__(self, model_path='models/l_version_1_300.pt'):
        """
        Initializes the YOLOv8 face and mask detector.
        :param model_path: Path to the YOLO model weights.
        """
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        
        if not os.path.isabs(model_path):
            model_path = os.path.join(project_root, model_path)

        try:
            self.model = YOLO(model_path)
        except Exception as e:
            print(f"Error loading model {model_path}: {e}")
            fallback = os.path.join(project_root, 'models', 'l_version_1_300.pt')
            print(f"Falling back to {fallback}")
            self.model = YOLO(fallback)

    def detect_faces(self, frame):
        """
        Detects faces and masks in a given frame.
        :param frame: OpenCV image (BGR).
        :return: List of face bounding boxes with confidence and optional spoof flag.
        """
        results = self.model(frame, verbose=False)
        faces = []
        
        for result in results:
            boxes = result.boxes
            for box in boxes:
                cls = int(box.cls[0])
                conf = float(box.conf[0])
                
                # new weights l_version_1_300.pt: 0 = 'fake', 1 = 'real'
                if conf > 0.35:
                    # Disable YOLO's buggy mask spoof classification to rely on the dedicated antispoof model
                    is_mask_spoof = False
                    xyxy = box.xyxy[0].tolist()
                    faces.append({
                        'bbox': [int(x) for x in xyxy],
                        'confidence': conf,
                        'is_mask_spoof': is_mask_spoof
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
    detector = YoloSegDetector()
    print("YoloSegDetector initialized successfully.")
