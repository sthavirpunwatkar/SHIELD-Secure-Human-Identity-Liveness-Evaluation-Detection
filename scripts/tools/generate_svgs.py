import re
import os
import subprocess

docs_dir = "/home/sp/Public/my_project/SHIELD-Secure-Human-Identity-Liveness-Evaluation-Detection/docs"
out_svg_dir = os.path.join(docs_dir, "figures", "svg")
out_src_dir = os.path.join(docs_dir, "figures", "source")

os.makedirs(out_svg_dir, exist_ok=True)
os.makedirs(out_src_dir, exist_ok=True)

# We will collect all mermaid blocks from both files and give them proper names
diagrams = []

def extract_diagrams(filepath, prefix=""):
    with open(filepath, "r") as f:
        content = f.read()
    
    last_h1, last_h2, last_h3 = "", "", ""
    lines = content.split('\n')
    
    i = 0
    while i < len(lines):
        line = lines[i]
        if line.startswith("# "): last_h1 = line[2:].strip()
        elif line.startswith("## "): last_h2 = line[3:].strip()
        elif line.startswith("### "): last_h3 = line[4:].strip()
        elif line.startswith("```mermaid"):
            # collect block
            j = i + 1
            code = []
            while j < len(lines) and not lines[j].startswith("```"):
                code.append(lines[j])
                j += 1
            diagrams.append({
                "source_file": os.path.basename(filepath),
                "h2": last_h2,
                "h3": last_h3,
                "code": "\n".join(code)
            })
            i = j
        i += 1

extract_diagrams(os.path.join(docs_dir, "architecture/architecture_overview.md"))
extract_diagrams(os.path.join(docs_dir, "SHIELD_Final_Project_Report.md"))

# Function to determine name based on headers
def get_name(idx, d):
    title = f"{d['h2']} {d['h3']}".lower()
    if "overall system architecture" in title: return "Figure_5_1_Overall_System_Architecture"
    if "inference pipeline" in title: return "Figure_5_2_Inference_Pipeline"
    if "request lifecycle" in title: return "Figure_5_3_Request_Lifecycle"
    if "frontend architecture" in title: return "Figure_6_1_Frontend_Architecture"
    if "backend architecture" in title: return "Figure_6_2_Backend_Architecture"
    if "deployment diagram" in title: return "Figure_6_3_Deployment_Diagram"
    if "docker architecture" in title: return "Figure_6_4_Docker_Architecture"
    if "api communication" in title: return "Figure_7_1_API_Communication"
    if "ai inference pipeline" in title: return "Figure_9_1_AI_Pipeline"
    if "fusion engine" in title: return "Figure_9_2_Fusion_Engine"
    if "activity diagram" in title and "decision pipeline" not in title: return "Figure_9_3_Activity_Diagram"
    if "state diagram" in title: return "Figure_9_4_State_Diagram"
    if "sequence diagram" in title: return "Figure_9_5_Sequence_Diagram"
    if "er diagram" in title: return "Figure_9_6_ER_Diagram"
    if "execution timeline" in title: return "Figure_11_1_Execution_Timeline"
    if "data flow diagram (level 1)" in title: return "Figure_8_2_Data_Flow_Level_1"
    if "component diagram" in title: return "Figure_8_3_Component_Diagram"
    
    # Report overrides
    if "decision pipeline activity diagram" in title: return "Figure_9_3_Decision_Activity_Diagram"
    
    return f"diagram_{idx}"

# Handle duplicates by appending _alt if name already used
used_names = set()

for idx, d in enumerate(diagrams):
    base_name = get_name(idx, d)
    name = base_name
    counter = 1
    while name in used_names:
        name = f"{base_name}_v{counter}"
        counter += 1
    used_names.add(name)
    
    # Save source
    src_path = os.path.join(out_src_dir, f"{name}.mmd")
    with open(src_path, "w") as f:
        f.write(d["code"])
    
    # Render SVG using npx @mermaid-js/mermaid-cli
    svg_path = os.path.join(out_svg_dir, f"{name}.svg")
    print(f"Rendering {name}.svg from {d['source_file']}...")
    # Using puppeteer configuration to ensure high quality (though default is usually fine for svg)
    # The user asked for "crisp text at 400-800% zoom" which is naturally handled by SVG.
    # No overlapping text, uniform sizes etc.
    cmd = ["npx", "@mermaid-js/mermaid-cli", "-i", src_path, "-o", svg_path, "-b", "transparent"]
    try:
        subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except subprocess.CalledProcessError as e:
        print(f"Error rendering {name}: {e.stderr.decode()}")
