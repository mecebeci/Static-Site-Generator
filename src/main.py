import os
import shutil
import sys

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

def generate_page(from_path, template_path, dest_path, basepath):
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
    template = template.replace('href="/', 'href="' + basepath)
    template = template.replace('src="/', 'src="' + basepath)

    # Ensure destination directory exists
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)

    with open(dest_path, "w") as dest_file:
        dest_file.write(template)
    
def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    for root, dirs, files in os.walk(dir_path_content):
        for file in files:
            if file.lower().endswith(".md"):
                # Full path to the markdown file
                from_path = os.path.join(root, file)

                # Relative path from content root
                rel_path = os.path.relpath(from_path, dir_path_content)

                # Change extension to .html
                rel_html_path = os.path.splitext(rel_path)[0] + ".html"

                # Destination path
                dest_path = os.path.join(dest_dir_path, rel_html_path)

                # Generate the HTML file
                generate_page(from_path, template_path, dest_path, basepath)


def main():
    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"
    copy_dir_recursive("static", "docs")
    generate_pages_recursive("content", "template.html", "docs", basepath)

if __name__ == "__main__":
    main()