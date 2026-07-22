import os
import subprocess

png_dir = "/home/sp/Public/my_project/SHIELD-Secure-Human-Identity-Liveness-Evaluation-Detection/docs/figures/labeled_for_pdf"
jpg_dir = "/home/sp/Downloads/jpg"
downloads_dir = "/home/sp/Downloads"

os.makedirs(jpg_dir, exist_ok=True)

for f in os.listdir(png_dir):
    if f.endswith(".png"):
        name = f[:-4]
        png_path = os.path.join(png_dir, f)
        jpg_path1 = os.path.join(jpg_dir, f"{name}.jpg")
        jpg_path2 = os.path.join(downloads_dir, f"{name}.jpg")
        print(f"Converting {f} to JPG...")
        cmd = ["magick", png_path, "-background", "white", "-flatten", jpg_path1]
        try:
            subprocess.run(cmd, check=True)
            subprocess.run(["cp", jpg_path1, jpg_path2], check=True)
        except Exception as e:
            print(f"Error converting {f}: {e}")

