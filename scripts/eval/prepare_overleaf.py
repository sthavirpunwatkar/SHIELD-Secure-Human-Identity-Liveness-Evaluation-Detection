import re
import os
import shutil

tex_file = "SHIELD_Final_Report_Placeholders.tex"
with open(tex_file, 'r') as f:
    content = f.read()

# We need to find blocks of figure to extract the meaningful filename and the original diagram ID
# Example:
# File Name:\\
# \texttt{Figure\_8\_1\_Overall\_System\_Architecture.pdf}\\
# ...
# \label{fig:diag_1}

os.makedirs("Figures", exist_ok=True)

blocks = re.findall(r'\\begin\{figure\}.*?\\end\{figure\}', content, re.DOTALL)
for block in blocks:
    m_file = re.search(r'File Name:\\\\\s*\\texttt\{(.*?)\}', block)
    m_label = re.search(r'\\label\{fig:diag_(\d+)\}', block)
    
    if m_file and m_label:
        meaningful_name = m_file.group(1).replace(r'\_', '_')
        diag_id = m_label.group(1)
        
        src_pdf = f"docs/images/diagram_{diag_id}.pdf"
        dest_pdf = f"Figures/{meaningful_name}"
        
        if os.path.exists(src_pdf):
            shutil.copy(src_pdf, dest_pdf)
            print(f"Copied {src_pdf} to {dest_pdf}")

# Copy the cdac-logo.png as well, since it's needed for the title page
if os.path.exists("docs/cdac-logo.png"):
    shutil.copy("docs/cdac-logo.png", "Figures/cdac-logo.png")
    # Wait, the tex file includes it as \includegraphics{cdac-logo.png} or \includegraphics{Figures/cdac-logo.png}?
    # In SHIELD_Project_Report.tex it is \includegraphics[height=3.5cm]{cdac-logo.png}
    # So we should also keep it in the root of the overleaf zip.
    shutil.copy("docs/cdac-logo.png", "cdac-logo.png")

print("Files copied.")
