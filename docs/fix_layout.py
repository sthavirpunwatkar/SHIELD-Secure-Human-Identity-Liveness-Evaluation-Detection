import re
import os

landscape_diagrams = [1, 2, 5, 7, 11, 12, 13, 14, 16]

files_to_fix = [
    'chapters_6_7.tex',
    'chapters_8.tex',
    'chapters_10.tex'
]

for filepath in files_to_fix:
    with open(filepath, 'r') as f:
        content = f.read()
    
    # First, fix the duplicate captions:
    # \caption{Figure 6.1: Frontend Architecture} -> \caption{Frontend Architecture}
    content = re.sub(r'\\caption\{Figure \d+\.\d+: (.*?)\}', r'\\caption{\1}', content)

    # Now, find all figure blocks and replace them entirely
    # The pattern matches \begin{figure}... \end{figure}
    
    def replacer(match):
        block = match.group(0)
        # Extract diagram number
        m_diag = re.search(r'diagram_(\d+)\.pdf', block)
        if not m_diag:
            return block
        diag_id = int(m_diag.group(1))
        
        # Extract caption
        m_cap = re.search(r'\\caption\{(.*?)\}', block)
        caption = m_cap.group(1) if m_cap else ""
        
        if diag_id in landscape_diagrams:
            # Landscape
            return (f"\\begin{{sidewaysfigure}}\n"
                    f"\\centering\n"
                    f"\\includegraphics[width=0.95\\textheight,height=0.95\\textwidth,keepaspectratio]{{images/diagram_{diag_id}.pdf}}\n"
                    f"\\caption{{{caption}}}\n"
                    f"\\end{{sidewaysfigure}}")
        else:
            # Portrait
            return (f"\\begin{{figure}}[p]\n"
                    f"\\centering\n"
                    f"\\includegraphics[width=0.95\\textwidth,height=0.95\\textheight,keepaspectratio]{{images/diagram_{diag_id}.pdf}}\n"
                    f"\\caption{{{caption}}}\n"
                    f"\\end{{figure}}")

    # Replace figure blocks
    # Note: need to handle \makebox or \fcolorbox that might be there now
    content = re.sub(r'\\begin\{figure\}[\s\S]*?\\end\{figure\}', replacer, content)

    with open(filepath, 'w') as f:
        f.write(content)

# Also add \usepackage{rotating} to SHIELD_Project_Report.tex
with open('SHIELD_Project_Report.tex', 'r') as f:
    main_tex = f.read()

if r'\usepackage{rotating}' not in main_tex:
    main_tex = main_tex.replace(r'\usepackage{lscape}', r'\usepackage{lscape}' + '\n' + r'\usepackage{rotating}')
    with open('SHIELD_Project_Report.tex', 'w') as f:
        f.write(main_tex)

print("Layout fixed.")
