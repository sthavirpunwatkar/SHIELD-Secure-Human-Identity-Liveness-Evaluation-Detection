import os
import subprocess

docs_dir = "/home/sp/Public/my_project/SHIELD-Secure-Human-Identity-Liveness-Evaluation-Detection/docs"
src_dir = os.path.join(docs_dir, "figures", "source")
png_dir = os.path.join(docs_dir, "figures", "png")
css_path = os.path.join(docs_dir, "figures", "style.css")

os.makedirs(png_dir, exist_ok=True)

for f in os.listdir(src_dir):
    if f.endswith(".mmd"):
        name = f[:-4]
        src_path = os.path.join(src_dir, f)
        png_path = os.path.join(png_dir, f"{name}.png")
        print(f"Rendering {name}.png with CSS...")
        cmd = ["npx", "@mermaid-js/mermaid-cli", "-i", src_path, "-o", png_path, "-C", css_path, "-b", "white", "-s", "3"]
        try:
            subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        except subprocess.CalledProcessError as e:
            print(f"Error rendering {name}: {e.stderr.decode()}")

