import os
import shutil

from nodes.textnode import TextNode, TextType
from functions import split_nodes_image

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


def main():
    # text_node = TextNode("This is some anchor text", "link", "https://boot.dev")
    # print(text_node)

    # test_str = "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)"
    # nodes = [TextNode(test_str, TextType.TEXT)]
    # result = split_nodes_image(nodes)
    # for node in result:
    #     print(node)

    copy_dir_recursive("static", "public")


if __name__ == "__main__":
    main()