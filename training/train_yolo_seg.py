from ultralytics import YOLO
import os

def train_yolo_seg(data_yaml="data/face_mask_seg.yaml", epochs=50, imgsz=640, model_name="yolov8n-seg.pt"):
    """
    Trains YOLOv8-seg on a custom face + mask dataset.
    Exports the resulting model to ONNX for production inference.
    """
    print(f"Loading pretrained model: {model_name}")
    model = YOLO(model_name)
    
    print(f"Starting training on {data_yaml} for {epochs} epochs...")
    results = model.train(
        data=data_yaml,
        epochs=epochs,
        imgsz=imgsz,
        project="training/runs",
        name="face_mask_seg"
    )
    
    print("Training completed. Exporting best model to ONNX...")
    # best.pt will be in training/runs/face_mask_seg/weights/best.pt
    export_path = model.export(format="onnx")
    print(f"ONNX model exported to: {export_path}")
    
if __name__ == "__main__":
    # Ensure data.yaml exists or adjust path appropriately
    data_yaml_path = os.path.join("data", "face_mask_seg.yaml")
    if not os.path.exists(data_yaml_path):
        print(f"Warning: {data_yaml_path} not found. Please create it before running.")
    
    train_yolo_seg(data_yaml=data_yaml_path)
