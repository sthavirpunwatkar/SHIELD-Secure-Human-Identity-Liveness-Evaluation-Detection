import re

with open("/home/sp/Public/my_project/SHIELD-Secure-Human-Identity-Liveness-Evaluation-Detection/docs/architecture/architecture_overview.md", "r") as f:
    content = f.read()

# find all headers and mermaid blocks
# split by lines and track last seen header
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
        print(f"Index {mermaid_idx}: H1: {last_h1} | H2: {last_h2} | H3: {last_h3}")
        # print first few lines of mermaid code
        j = i + 1
        print("  Code snippet: ", end="")
        while j < i + 3 and j < len(lines):
            print(lines[j], end=" ")
            j += 1
        print("\n")
        mermaid_idx += 1
