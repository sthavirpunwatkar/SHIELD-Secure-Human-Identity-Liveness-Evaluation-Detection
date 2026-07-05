import os
import cv2
import numpy as np
import shutil
import urllib.request
import zipfile
import argparse
from pathlib import Path
import random

def download_mock_dataset(download_dir):
    """
    Since CASIA-SURF and HKBU require signed agreements and registration,
    we create a mock dataset to demonstrate the conversion process.
    If you have the actual dataset, extract it to 'data/raw_masks/'.
    """
    print("Creating mock dataset for demonstration...")
    raw_dir = download_dir / 'raw_masks'
    images_dir = raw_dir / 'images'
    masks_dir = raw_dir / 'masks'
    
    images_dir.mkdir(parents=True, exist_ok=True)
    masks_dir.mkdir(parents=True, exist_ok=True)
    
    for i in range(10):
        # Create dummy image
        img = np.zeros((480, 640, 3), dtype=np.uint8)
        cv2.rectangle(img, (100, 100), (540, 380), (255, 200, 200), -1)
        
        # Create dummy mask (1 = mask, 0 = real face for this example, let's alternate)
        mask = np.zeros((480, 640), dtype=np.uint8)
        label_class = 1 if i % 2 == 0 else 0 # 1 for mask, 0 for face
        
        # Draw a blob on the mask
        cv2.circle(mask, (320, 240), 100, 255, -1)
        
        # Save them
        cv2.imwrite(str(images_dir / f"sample_{i}.jpg"), img)
        cv2.imwrite(str(masks_dir / f"sample_{i}_{label_class}.png"), mask)

    print(f"Mock dataset created at {raw_dir}")
    return raw_dir

def extract_polygons_from_mask(mask, class_id, img_width, img_height):
    """
    Extract polygons from a binary mask for YOLOv8-seg.
    """
    # Ensure binary mask
    _, binary = cv2.threshold(mask, 127, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    lines = []
    for contour in contours:
        if cv2.contourArea(contour) < 50:
            continue
            
        epsilon = 0.002 * cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, epsilon, True)
        
        polygon = []
        for point in approx:
            x, y = point[0]
            norm_x = min(max(x / img_width, 0.0), 1.0)
            norm_y = min(max(y / img_height, 0.0), 1.0)
            polygon.extend([f"{norm_x:.6f}", f"{norm_y:.6f}"])
            
        if len(polygon) >= 6: # Triangle or more
            line = f"{class_id} " + " ".join(polygon)
            lines.append(line)
            
    return lines

def convert_to_yolo(raw_dir, output_dir):
    """
    Converts masks to YOLOv8-seg polygon format.
    Classes: 0=face, 1=mask.
    """
    print(f"Converting dataset from {raw_dir} to YOLOv8-seg format at {output_dir}...")
    
    images_dir = raw_dir / 'images'
    masks_dir = raw_dir / 'masks'
    
    # YOLO directories
    for split in ['train', 'val']:
        (output_dir / 'images' / split).mkdir(parents=True, exist_ok=True)
        (output_dir / 'labels' / split).mkdir(parents=True, exist_ok=True)
        
    image_files = list(images_dir.glob('*.jpg'))
    random.shuffle(image_files)
    
    split_idx = int(len(image_files) * 0.8)
    train_files = image_files[:split_idx]
    val_files = image_files[split_idx:]
    
    def process_split(files, split_name):
        for img_path in files:
            img = cv2.imread(str(img_path))
            h, w = img.shape[:2]
            
            # Find corresponding mask
            # For this script, we assume mask names are f"{img_name}_{class_id}.png"
            # In a real dataset like HKBU, parse the metadata or file structure to get the class and mask
            mask_paths = list(masks_dir.glob(f"{img_path.stem}_*.png"))
            
            label_lines = []
            for mask_path in mask_paths:
                try:
                    class_id = int(mask_path.stem.split('_')[-1])
                except ValueError:
                    class_id = 0 # default
                    
                mask = cv2.imread(str(mask_path), cv2.IMREAD_GRAYSCALE)
                if mask is not None:
                    lines = extract_polygons_from_mask(mask, class_id, w, h)
                    label_lines.extend(lines)
            
            # Copy image
            dest_img = output_dir / 'images' / split_name / img_path.name
            shutil.copy(img_path, dest_img)
            
            # Write labels
            label_path = output_dir / 'labels' / split_name / f"{img_path.stem}.txt"
            with open(label_path, 'w') as f:
                f.write("\n".join(label_lines))
                
    process_split(train_files, 'train')
    process_split(val_files, 'val')
    
    # Create data.yaml
    yaml_content = f"""path: {output_dir.absolute()}
train: images/train
val: images/val
test:  # test images (optional)

# Classes
names:
  0: face
  1: mask
"""
    with open(output_dir / 'data.yaml', 'w') as f:
        f.write(yaml_content)
        
    print(f"Conversion complete. Config saved to {output_dir / 'data.yaml'}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Prepare Silicone Mask Dataset for YOLOv8-seg")
    parser.add_argument("--data_dir", type=str, default="data", help="Base data directory")
    parser.add_argument("--mock", action="store_true", help="Generate mock dataset if real is unavailable")
    args = parser.parse_args()
    
    base_dir = Path(args.data_dir)
    yolo_dir = base_dir / 'yolo_mask_seg'
    
    raw_dir = base_dir / 'raw_masks'
    
    if args.mock or not raw_dir.exists():
        raw_dir = download_mock_dataset(base_dir)
        
    if raw_dir.exists():
        convert_to_yolo(raw_dir, yolo_dir)
        print("\nTo start training with YOLOv8, run:")
        print(f"yolo task=segment mode=train data={yolo_dir / 'data.yaml'} model=yolov8n-seg.pt epochs=50 imgsz=640")
    else:
        print("Raw dataset not found. Please extract your masks to data/raw_masks/ or run with --mock")
