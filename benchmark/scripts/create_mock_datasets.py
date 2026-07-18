import os
import cv2
import csv
import numpy as np

def create_datasets():
    base_dir = "benchmark/datasets"
    os.makedirs(base_dir, exist_ok=True)
    
    # Anti-Spoof
    fas_datasets = ["ReplayAttack", "CASIA", "MSU"]
    manifest = []
    
    for ds in fas_datasets:
        os.makedirs(os.path.join(base_dir, ds, "live"), exist_ok=True)
        os.makedirs(os.path.join(base_dir, ds, "spoof"), exist_ok=True)
        
        # 33 live, 33 spoof per dataset ~ 100 total each
        for i in range(34):
            live_path = os.path.join(base_dir, ds, "live", f"sample_{i}.jpg")
            spoof_path = os.path.join(base_dir, ds, "spoof", f"sample_{i}.jpg")
            
            img_live = np.random.randint(50, 255, (480, 640, 3), dtype=np.uint8)
            img_spoof = np.random.randint(0, 200, (480, 640, 3), dtype=np.uint8)
            
            # draw dummy face
            cv2.rectangle(img_live, (200, 150), (400, 350), (0, 255, 0), 2)
            cv2.rectangle(img_spoof, (200, 150), (400, 350), (0, 0, 255), 2)
            
            cv2.imwrite(live_path, img_live)
            cv2.imwrite(spoof_path, img_spoof)
            
            manifest.append([ds, "anti_spoof", "live", live_path])
            manifest.append([ds, "anti_spoof", "spoof", spoof_path])

    # rPPG
    rppg_datasets = ["UBFC", "PURE"]
    for ds in rppg_datasets:
        os.makedirs(os.path.join(base_dir, ds, "videos"), exist_ok=True)
        # 5-10 sequences per dataset
        for i in range(5):
            video_path = os.path.join(base_dir, ds, "videos", f"seq_{i}")
            os.makedirs(video_path, exist_ok=True)
            for f in range(32):
                frame_path = os.path.join(video_path, f"frame_{f:03d}.jpg")
                img = np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)
                cv2.imwrite(frame_path, img)
            manifest.append([ds, "rppg", "sequence", video_path])

    with open(os.path.join(base_dir, "dataset_manifest.csv"), "w") as f:
        writer = csv.writer(f)
        writer.writerow(["dataset", "type", "label", "path"])
        writer.writerows(manifest)

if __name__ == "__main__":
    create_datasets()
