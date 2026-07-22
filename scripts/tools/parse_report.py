import re

with open("/home/sp/Public/my_project/SHIELD-Secure-Human-Identity-Liveness-Evaluation-Detection/docs/SHIELD_Final_Project_Report.md", "r") as f:
    content = f.read()

last_h1 = ""
last_h2 = ""
last_h3 = ""

lines = content.split('\n')
mermaid_idx = 0
for i, line in enumerate(lines):
    if line.startswith("# "): last_h1 = line[2:]
    elif line.startswith("## "): last_h2 = line[3:]
    elif line.startswith("### "): last_h3 = line[4:]
    elif line.startswith("```mermaid"):
        print(f"Report Index {mermaid_idx}: H1: {last_h1} | H2: {last_h2} | H3: {last_h3}")
        j = i + 1
        print("  Code snippet: ", end="")
        while j < i + 3 and j < len(lines):
            print(lines[j], end=" ")
            j += 1
        print("\n")
        mermaid_idx += 1
