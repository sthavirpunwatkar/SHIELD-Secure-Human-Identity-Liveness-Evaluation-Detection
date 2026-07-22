import glob

for f in glob.glob('*.tex'):
    with open(f, 'r') as file:
        content = file.read()
    content = content.replace(r'\texttt{diagram_', r'\texttt{diagram\_')
    with open(f, 'w') as file:
        file.write(content)
print("Underscores escaped.")
