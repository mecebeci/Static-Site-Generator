import os
import shutil

from nodes.textnode import TextNode, TextType
from functions import *

def copy_dir_recursive(source, destination):
    # Ensure destination exists and clean
    if os.path.exists(destination):
        shutil.rmtree(destination)
    os.makedirs(destination)

    # Walk through source directory
    for item in os.listdir(source):
        source_path = os.path.join(source, item)
        destination_path = os.path.join(destination, item)

        if os.path.isdir(source_path):
            # Recursively copy subdirectory
            copy_dir_recursive(source_path, destination_path)
        else:
            # Copy file
            shutil.copy2(source_path, destination_path)
            print(f"Copied file: {destination_path}")


def extract_title(markdown):
    lines = markdown.splitlines()
    header = None
    for line in lines:
        line = line.strip()
        if line[:2] == "# ":
            header = line[2:]
            return header
    if not header:
        raise Exception("There is no header!")

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    if not os.path.isfile(from_path):
        raise FileNotFoundError(f"The file '{from_path}' does not exist.")
    with open(from_path, "r") as from_path_file:
        markdown = from_path_file.read()

    if not os.path.isfile(template_path):
        raise FileNotFoundError(f"The file '{template_path} does not exist.'")
    with open(template_path, "r") as template_path_file:
        template = template_path_file.read()

    html_string = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)

    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html_string)

    # Ensure destination directory exists
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)

    with open(dest_path, "w") as dest_file:
        dest_file.write(template)
    
def main():
    copy_dir_recursive("static", "public")
    generate_page("content/index.md", "template.html", "public/index.html")

if __name__ == "__main__":
    main()