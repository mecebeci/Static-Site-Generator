from nodes.textnode import TextNode, TextType
from functions import split_nodes_image
def main():
    # text_node = TextNode("This is some anchor text", "link", "https://boot.dev")
    # print(text_node)
    test_str = "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)"
    nodes = [TextNode(test_str, TextType.TEXT)]
    result = split_nodes_image(nodes)
    for node in result:
        print(node)

if __name__ == "__main__":
    main()