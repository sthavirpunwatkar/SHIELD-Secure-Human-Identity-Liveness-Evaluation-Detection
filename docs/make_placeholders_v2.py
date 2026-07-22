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
        
        m_cap = re.search(r'\\caption\{(.*?)\}', block, re.DOTALL)
        full_caption = m_cap.group(1).strip() if m_cap else ""
        
        # Remove duplicate prefix if it already exists e.g. "Figure 8.1: Figure 8.1: Foo"
        # Not needed since we're starting from base, but good to be safe.
        full_caption = re.sub(r'^(Figure\s+\d+\.\d+:\s*)+(Figure\s+\d+\.\d+:)', r'\2', full_caption)

        m_title = re.match(r'(Figure\s+\d+\.\d+):\s*(.*)', full_caption, re.IGNORECASE)
        
        if m_title:
            fig_num = m_title.group(1) # "Figure 8.1"
            fig_title = m_title.group(2) # "Overall System Architecture"
            
            clean_caption_for_latex = fig_title
            
            safe_title = re.sub(r'[^A-Za-z0-9]+', '_', fig_title)
            fig_num_str = re.sub(r'[^A-Za-z0-9]+', '_', fig_num)
            meaningful_filename = f"{fig_num_str}_{safe_title}.pdf"
            display_caption = full_caption
        else:
            clean_caption_for_latex = full_caption
            safe_title = re.sub(r'[^A-Za-z0-9]+', '_', full_caption)
            meaningful_filename = f"{safe_title}.pdf"
            display_caption = full_caption
            
        m_lbl = re.search(r'\\label\{.*?\}', block)
        label_cmd = m_lbl.group(0) if m_lbl else f"\\label{{fig:diag_{diag_id}}}"
        
        orientation = "Portrait" # Default as requested, or determine from landscape_diagrams
        if diag_id in landscape_diagrams:
            orientation = "Landscape"
            
        meaningful_filename_esc = meaningful_filename.replace('_', r'\_')
            
        placeholder = f"""\\begin{{center}}
----------------------------------------------------------\\\\
\\vspace{{0.5em}}
\\textbf{{INSERT THE FOLLOWING FIGURE}}\\\\
\\vspace{{1em}}
File Name:\\\\
\\texttt{{{meaningful_filename_esc}}}\\\\
\\vspace{{1em}}
Folder:\\\\
\\texttt{{Figures/}}\\\\
\\vspace{{1em}}
Caption:\\\\
{display_caption}\\\\
\\vspace{{1em}}
Orientation:\\\\
{orientation}\\\\
\\vspace{{1em}}
Suggested Width:\\\\
90\\% of printable page\\\\
\\vspace{{3cm}}
----------------------------------------------------------
\\end{{center}}"""
        
        new_block = f"\\begin{{figure}}[htbp]\n{placeholder}\n\\caption{{{clean_caption_for_latex}}}\n{label_cmd}\n\\end{{figure}}"
        return new_block

    new_content = re.sub(r'\\begin\{figure\}[\s\S]*?\\end\{figure\}', replacer, content)
    new_content = re.sub(r'\\begin\{sidewaysfigure\}[\s\S]*?\\end\{sidewaysfigure\}', replacer, new_content)
    new_content = re.sub(r'\\begin\{landscape\}\s*(\\begin\{figure\}[\s\S]*?\\end\{figure\})\s*\\end\{landscape\}', r'\1', new_content)

    with open(filepath, 'w') as f:
        f.write(new_content)

tex_files = glob.glob('*.tex')
for f in tex_files:
    process_file(f)

print("Placeholders V2 generated.")
