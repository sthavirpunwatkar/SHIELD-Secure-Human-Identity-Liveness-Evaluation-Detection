from ultralytics import YOLO
import os

project_root = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(project_root, 'models', 'l_version_1_300.pt')
model = YOLO(model_path)
print("Classes:", model.names)
