import cv2
import numpy as np
import os
from ultralytics import YOLO

class YoloSegDetector:
    def __init__(self, model_path='models/yolov8n-seg.pt'):
        """
        Initializes the YOLOv8-seg face and mask detector.
        :param model_path: Path to the YOLOv8-seg model weights.
        """
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        
        if not os.path.isabs(model_path):
            model_path = os.path.join(project_root, model_path)

        try:
            self.model = YOLO(model_path)
        except Exception as e:
            print(f"Error loading model {model_path}: {e}")
            fallback = os.path.join(project_root, 'models', 'yolov8n-seg.pt')
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
        mask_spoof_detected = False
        
        for result in results:
            boxes = result.boxes
            for box in boxes:
                cls = int(box.cls[0])
                conf = float(box.conf[0])
                
                # Assume class 1 is 'mask' for spoofing (e.g., silicone mask or physical mask spoof)
                if cls == 1 and conf > 0.60:
                    mask_spoof_detected = True
                
                # Assume class 0 is 'face'
                if cls == 0 and conf > 0.35:
                    xyxy = box.xyxy[0].tolist()
                    faces.append({
                        'bbox': [int(x) for x in xyxy],
                        'confidence': conf,
                        'is_mask_spoof': mask_spoof_detected
                    })
        
        # If any face is found, we can attach the spoof detected flag to it
        for face in faces:
            face['is_mask_spoof'] = mask_spoof_detected
            
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
