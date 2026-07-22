import os
import subprocess

svg_dir = "/home/sp/Downloads/svg/"
png_dir = "/home/sp/Downloads/png/"
downloads_dir = "/home/sp/Downloads/"

for f in os.listdir(svg_dir):
    if f.endswith(".svg"):
        name = f[:-4]
        svg_path = os.path.join(svg_dir, f)
        png_path1 = os.path.join(png_dir, f"{name}.png")
        png_path2 = os.path.join(downloads_dir, f"{name}.png")
        print(f"Converting {f} to PNG...")
        # Add background white and flatten to ensure text is visible on transparent SVGs
        # If the text was black, it will be visible on white.
        cmd = ["magick", "-density", "300", "-background", "white", svg_path, "-flatten", png_path1]
        try:
            subprocess.run(cmd, check=True)
            subprocess.run(["cp", png_path1, png_path2], check=True)
        except Exception as e:
            print(f"Error converting {f}: {e}")

