from ultralytics import YOLO

model = YOLO('models/l_version_1_300.pt')
print("Model Task:", model.task)
print("Model Names:", model.names)
