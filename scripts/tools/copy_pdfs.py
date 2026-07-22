import os
import shutil

docs_dir = "/home/sp/Public/my_project/SHIELD-Secure-Human-Identity-Liveness-Evaluation-Detection/docs"
images_dir = os.path.join(docs_dir, "images")
pdf_dir = os.path.join(docs_dir, "figures", "pdf")
source_dir = os.path.join(docs_dir, "figures", "source")

os.makedirs(pdf_dir, exist_ok=True)

# First, read all generated source MMDs to build a dictionary of content -> Name
# To handle slight whitespace differences, we strip all whitespace.
def normalize(text):
    return "".join(text.split())

content_to_name = {}
for file in os.listdir(source_dir):
    if file.endswith(".mmd"):
        name = file[:-4]
        with open(os.path.join(source_dir, file), "r") as f:
            content = f.read()
            content_to_name[normalize(content)] = name

# Now iterate through images dir
mapped = 0
for file in os.listdir(images_dir):
    if file.endswith(".mmd"):
        with open(os.path.join(images_dir, file), "r") as f:
            content = f.read()
        
        norm_content = normalize(content)
        if norm_content in content_to_name:
            target_name = content_to_name[norm_content]
            # Check if there is a corresponding PDF
            pdf_name = file[:-4] + ".pdf"
            pdf_path = os.path.join(images_dir, pdf_name)
            if os.path.exists(pdf_path):
                target_pdf_path = os.path.join(pdf_dir, target_name + ".pdf")
                shutil.copy(pdf_path, target_pdf_path)
                print(f"Copied {pdf_name} to {target_name}.pdf")
                mapped += 1
        else:
            print(f"Could not map {file}")

print(f"Total PDFs mapped: {mapped}")
