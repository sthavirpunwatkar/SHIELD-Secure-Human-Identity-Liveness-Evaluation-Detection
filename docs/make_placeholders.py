import re
import os
import glob

landscape_diagrams = [1, 2, 5, 7, 11, 12, 13, 14, 16]

def process_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    def replacer(match):
        block = match.group(0)
        
        m_diag = re.search(r'diagram_(\d+)\.(pdf|png)', block)
        if not m_diag:
            return block
        diag_id = int(m_diag.group(1))
        ext = m_diag.group(2)
        actual_filename = f"diagram_{diag_id}.{ext}"
        
        m_cap = re.search(r'\\caption\{(.*?)\}', block, re.DOTALL)
        caption_text = m_cap.group(1).strip() if m_cap else ""
        
        m_lbl = re.search(r'\\label\{.*?\}', block)
        label_cmd = m_lbl.group(0) if m_lbl else f"\\label{{fig:diag_{diag_id}}}"
        
        orientation = "Landscape" if diag_id in landscape_diagrams else "Portrait"
        
        placeholder = f"""\\begin{{center}}
==================================================\\\\
\\textbf{{[ INSERT FIGURE HERE ]}}\\\\
\\vspace{{0.5em}}
Actual File Name: \\texttt{{{actual_filename}}}\\\\
Caption: {caption_text}\\\\
Source Folder: \\texttt{{images/}}\\\\
Recommended Orientation: {orientation}\\\\
Recommended Width: 90\\% of printable page\\\\
\\vspace{{0.5em}}
\\textit{{Replace this placeholder with the corresponding PDF vector figure.}}\\\\
==================================================
\\end{{center}}"""
        
        new_block = f"\\begin{{figure}}[htbp]\n{placeholder}\n\\caption{{{caption_text}}}\n{label_cmd}\n\\end{{figure}}"
        return new_block

    new_content = re.sub(r'\\begin\{figure\}[\s\S]*?\\end\{figure\}', replacer, content)
    new_content = re.sub(r'\\begin\{sidewaysfigure\}[\s\S]*?\\end\{sidewaysfigure\}', replacer, new_content)
    new_content = re.sub(r'\\begin\{landscape\}\s*(\\begin\{figure\}[\s\S]*?\\end\{figure\})\s*\\end\{landscape\}', r'\1', new_content)

    with open(filepath, 'w') as f:
        f.write(new_content)

tex_files = glob.glob('*.tex')
for f in tex_files:
    process_file(f)
