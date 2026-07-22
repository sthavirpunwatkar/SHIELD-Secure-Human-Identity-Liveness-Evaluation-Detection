import os
import shutil
import re

docs_dir = "/home/sp/Public/my_project/SHIELD-Secure-Human-Identity-Liveness-Evaluation-Detection/docs"
pdf_dir = os.path.join(docs_dir, "figures", "pdf")
svg_dir = os.path.join(docs_dir, "figures", "svg")

target_dir = os.path.join(docs_dir, "figures", "labeled_for_pdf")

def map_name(current):
    curr_lower = current.lower().replace("_", " ")
    if "frontend architecture" in curr_lower: return "Figure 6 1 Frontend Architecture"
    if "backend architecture" in curr_lower: return "Figure 6 2 Backend Architecture"
    if "deployment diagram" in curr_lower: return "Figure 6 3 Deployment Diagram"
    if "docker architecture" in curr_lower: return "Figure 6 4 Docker Architecture"
    if "api communication" in curr_lower: return "Figure 7 2 API Communication"
    if "overall system architecture" in curr_lower and "report" not in curr_lower: return "Figure 8 1 Overall System Architecture"
    if "data flow" in curr_lower: return "Figure 8 2 Data Flow Diagram Level 1 "
    if "ai pipeline" in curr_lower or "inference pipeline" in curr_lower: return "Figure 8 3 Inference Pipeline"
    if "fusion engine" in curr_lower: return "Figure 8 4 Fusion Engine"
    if "activity diagram" in curr_lower and "decision" not in curr_lower: return "Figure 8 5 Activity Diagram"
    if "state diagram" in curr_lower: return "Figure 8 6 Session State Diagram"
    if "sequence diagram" in curr_lower: return "Figure 10 1 WebSocket Sequence Diagram"
    if "execution timeline" in curr_lower: return "Figure 10 2 Execution Timeline"
    return None

def process_dir(src_dir, ext):
    if not os.path.exists(src_dir): return
    for f in os.listdir(src_dir):
        if f.endswith(ext):
            mapped = map_name(f)
            if mapped:
                src = os.path.join(src_dir, f)
                dst = os.path.join(target_dir, mapped + ext)
                shutil.copy(src, dst)
                print(f"Copied {f} to {mapped}{ext}")

process_dir(svg_dir, ".svg")
process_dir(pdf_dir, ".pdf")
