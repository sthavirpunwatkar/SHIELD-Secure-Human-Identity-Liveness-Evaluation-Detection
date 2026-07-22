import os
import subprocess

docs_dir = "/home/sp/Public/my_project/SHIELD-Secure-Human-Identity-Liveness-Evaluation-Detection/docs"
out_svg_dir = os.path.join(docs_dir, "figures", "svg")
out_src_dir = os.path.join(docs_dir, "figures", "source")

def process_file(filepath, base_name):
    with open(filepath, "r") as f:
        content = f.read()
    
    lines = content.split('\n')
    idx = 0
    i = 0
    while i < len(lines):
        line = lines[i]
        if line.startswith("```mermaid"):
            j = i + 1
            code = []
            while j < len(lines) and not lines[j].startswith("```"):
                code.append(lines[j])
                j += 1
            
            name = f"{base_name}" if idx == 0 else f"{base_name}_{idx}"
            src_path = os.path.join(out_src_dir, f"{name}.mmd")
            with open(src_path, "w") as out_f:
                out_f.write("\n".join(code))
                
            svg_path = os.path.join(out_svg_dir, f"{name}.svg")
            print(f"Rendering {name}.svg")
            subprocess.run(["npx", "@mermaid-js/mermaid-cli", "-i", src_path, "-o", svg_path, "-b", "transparent"], check=True)
            
            idx += 1
            i = j
        i += 1

process_file(os.path.join(docs_dir, "architecture/dependency_graph.md"), "Figure_10_1_Repository_Dependency_Graph")
process_file(os.path.join(docs_dir, "architecture/HARDWARE_ENCODER_EPIC.md"), "Figure_Hardware_Encoder_Epic")
process_file(os.path.join(docs_dir, "improvements.md"), "Figure_Improvements")
