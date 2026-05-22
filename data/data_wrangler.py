import os
import cv2
import json
from inference.quality import QualityScoreEngine

class DataWrangler:
    def __init__(self, output_base="data/processed"):
        """
        Initializes the Data Wrangler.
        :param output_base: Where to store standardized and filtered data.
        """
        self.output_base = output_base
        self.quality_engine = QualityScoreEngine()
        self.manifest = []

        if not os.path.exists(self.output_base):
            os.makedirs(self.output_base, exist_ok=True)

    def process_dataset(self, source_dir, dataset_name, label_map, is_video=True, strict=True):
        """
        Processes a dataset (video or image based).
        :param source_dir: Path to raw data.
        :param dataset_name: Label for the source.
        :param label_map: Dict mapping subfolders to 'live' or 'spoof'.
        :param is_video: Whether the source contains videos.
        :param strict: If True, only saves frames passing the Quality Gate.
        """
        print(f"--- Wrangling Dataset: {dataset_name} ---")
        
        for root, dirs, files in os.walk(source_dir):
            for file in files:
                # Determine label from path
                label = "unknown"
                for pattern, target in label_map.items():
                    if pattern in root.lower() or pattern in file.lower():
                        label = target
                        break
                
                if label == "unknown":
                    continue

                full_path = os.path.join(root, file)
                
                if is_video and file.endswith(('.mp4', '.avi', '.mov')):
                    self._process_video(full_path, dataset_name, label, strict)
                elif not is_video and file.endswith(('.jpg', '.png', '.jpeg')):
                    self._process_image(full_path, dataset_name, label, strict)

    def _process_video(self, video_path, dataset_name, label, strict):
        cap = cv2.VideoCapture(video_path)
        video_id = os.path.splitext(os.path.basename(video_path))[0]
        output_dir = os.path.join(self.output_base, dataset_name, label)
        os.makedirs(output_dir, exist_ok=True)

        frame_idx = 0
        saved = 0
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret: break
            
            # Sample every 10th frame to keep it lean
            if frame_idx % 10 == 0:
                h, w = frame.shape[:2]
                face_crop = frame[int(h*0.2):int(h*0.8), int(w*0.2):int(w*0.8)]
                
                res = self.quality_engine.evaluate(frame, face_crop)
                if not strict or res["passes_gate"]:
                    fname = f"{video_id}_f{frame_idx}.jpg"
                    fpath = os.path.join(output_dir, fname)
                    cv2.imwrite(fpath, frame)
                    self._add_to_manifest(fpath, dataset_name, label, res["quality_score"])
                    saved += 1
            frame_idx += 1
        cap.release()
        print(f"  Video {video_id}: Saved {saved} frames.")

    def _process_image(self, img_path, dataset_name, label, strict):
        frame = cv2.imread(img_path)
        if frame is None: return
        
        output_dir = os.path.join(self.output_base, dataset_name, label)
        os.makedirs(output_dir, exist_ok=True)
        
        h, w = frame.shape[:2]
        face_crop = frame[int(h*0.1):int(h*0.9), int(w*0.1):int(w*0.9)]
        
        res = self.quality_engine.evaluate(frame, face_crop)
        if not strict or res["passes_gate"]:
            fname = os.path.basename(img_path)
            fpath = os.path.join(output_dir, fname)
            cv2.imwrite(fpath, frame)
            self._add_to_manifest(fpath, dataset_name, label, res["quality_score"])

    def _add_to_manifest(self, path, dataset, label, score):
        self.manifest.append({
            "path": os.path.abspath(path),
            "dataset": dataset,
            "label": label,
            "quality_score": score
        })

    def save_manifest(self):
        mpath = os.path.join(self.output_base, "manifest.json")
        with open(mpath, 'w') as f:
            json.dump(self.manifest, f, indent=4)
        print(f"Manifest saved: {len(self.manifest)} samples.")

if __name__ == "__main__":
    wrangler = DataWrangler()
    print("DataWrangler initialized.")
