import os
import shutil

def split_data():
    base_dir = "/home/sp/Public/my_project/SHIELD-Secure-Human-Identity-Liveness-Evaluation-Detection"
    raw_dir = os.path.join(base_dir, "data/archive/raw")
    target_dir = os.path.join(base_dir, "data/NUAA")
    
    # Create directories
    splits = {
        "client_train_raw.txt": ("train", "real"),
        "client_test_raw.txt": ("test", "real"),
        "imposter_train_raw.txt": ("train", "spoof"),
        "imposter_test_raw.txt": ("test", "spoof")
    }
    
    for txt_file, (split_name, class_name) in splits.items():
        txt_path = os.path.join(raw_dir, txt_file)
        dest_dir = os.path.join(target_dir, split_name, class_name)
        os.makedirs(dest_dir, exist_ok=True)
        
        if not os.path.exists(txt_path):
            print(f"Error: {txt_path} not found.")
            continue
            
        print(f"Processing {txt_file} -> {dest_dir}...")
        
        with open(txt_path, 'r') as f:
            lines = f.readlines()
            
        count = 0
        copied = 0
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # Line looks like: /kaggle/input/nuaaaa/raw/ClientRaw/0001/0001_00_00_01_0.jpg
            # We want to find the relative part: ClientRaw/... or ImposterRaw/...
            parts = line.split('/')
            try:
                # Find where ClientRaw or ImposterRaw is in the path
                idx = -1
                for i, p in enumerate(parts):
                    if p in ["ClientRaw", "ImposterRaw"]:
                        idx = i
                        break
                if idx == -1:
                    print(f"Could not parse line: {line}")
                    continue
                    
                rel_path = "/".join(parts[idx:])
                src_path = os.path.join(raw_dir, rel_path)
                
                if os.path.exists(src_path):
                    # Destination filename
                    dest_file_name = "_".join(parts[idx+1:]) # E.g., 0001_0001_00_00_01_0.jpg to avoid collision
                    dest_path = os.path.join(dest_dir, dest_file_name)
                    
                    # Copy file
                    shutil.copy(src_path, dest_path)
                    copied += 1
                else:
                    # Let's check if there is a case sensitivity issue or different relative path
                    # Try direct match relative to raw_dir
                    pass
            except Exception as e:
                print(f"Error copying {line}: {e}")
                
            count += 1
            
        print(f"  Processed {count} lines, successfully copied {copied} files.")

if __name__ == "__main__":
    split_data()
