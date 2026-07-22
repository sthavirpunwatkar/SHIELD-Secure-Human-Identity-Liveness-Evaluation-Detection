import re
import subprocess
import os

with open('architecture/architecture_overview.md', 'r') as f:
    content = f.read()

# Find all mermaid blocks
pattern = re.compile(r'```mermaid\n(.*?)\n```', re.DOTALL)
matches = pattern.findall(content)

os.makedirs('images', exist_ok=True)

for i, match in enumerate(matches):
    mmd_path = f'images/diagram_{i+1}.mmd'
    pdf_path = f'images/diagram_{i+1}.pdf'
    
    with open(mmd_path, 'w') as f:
        f.write(match)
        
    print(f"Compiling {mmd_path}...")
    subprocess.run(['npx', '-y', '@mermaid-js/mermaid-cli', '-i', mmd_path, '-o', pdf_path, '-b', 'transparent'], check=False)
    
print("Done.")
