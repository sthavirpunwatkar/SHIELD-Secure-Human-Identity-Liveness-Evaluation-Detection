import os
import re

doc_dir = "/home/sp/Public/my_project/SHIELD-Secure-Human-Identity-Liveness-Evaluation-Detection/docs"
out_dir = "/home/sp/Public/my_project/SHIELD-Secure-Human-Identity-Liveness-Evaluation-Detection/docs/figures/source"

for root, dirs, files in os.walk(doc_dir):
    for file in files:
        if file.endswith(".md"):
            path = os.path.join(root, file)
            with open(path, "r") as f:
                content = f.read()
                matches = re.finditer(r"```mermaid\n(.*?)\n```", content, re.DOTALL)
                for i, match in enumerate(matches):
                    # Try to find a preceding header or caption
                    # Just save them as extracted_X_filename.mmd
                    out_path = os.path.join(out_dir, f"extracted_{file}_{i}.mmd")
                    with open(out_path, "w") as out_f:
                        out_f.write(match.group(1))
                    print(f"Extracted {out_path}")
