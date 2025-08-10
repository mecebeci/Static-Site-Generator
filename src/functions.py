import re
from nodes.textnode import *
from nodes.leafnode import *
from nodes.htmlnode import *
from nodes.parentnode import *
from nodes.blocktype import *

# Convert TextNodes into HTMLNodes
def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(tag=None, value=text_node.text)
        
        case TextType.BOLD:
            return LeafNode(tag="b", value=text_node.text)
        
        case TextType.ITALIC:
            return LeafNode(tag="i", value=text_node.text)
        
        case TextType.CODE:
            return LeafNode(tag="code",value=text_node.text)
        
        case TextType.LINK:
            return LeafNode(tag="a", value=text_node.text, props={"href":text_node.url})
        
        case TextType.IMAGE:
            return LeafNode(tag="img", value="", props={"src":text_node.url, "alt":text_node.text})
        
        case _:
            raise Exception("There is no such a type")
        

# Split Delimiter
def split_nodes_delimiter(old_nodes, delimiter, text_type):
    ret_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            ret_nodes.append(node)
            continue
        
        else:
            count = node.text.count(delimiter)
            if count % 2 != 0:
                raise Exception("Invalid Markdown syntax...")
            if count == 0:
                ret_nodes.append(node)
                continue

            text_list = node.text.split(delimiter)
            
            i = 0
            while i < len(text_list):
                if len(text_list[i]) == 0:
                    i += 1
                    continue
                if i % 2 == 0:
                    new_node = TextNode(text_list[i], TextType.TEXT)
                else:
                    new_node = TextNode(text_list[i], text_type)
                
                ret_nodes.append(new_node)
                i += 1
    return ret_nodes
            

def extract_markdown_images(text):
    tuple_list = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return tuple_list

def extract_markdown_links(text):
    tuple_list = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return tuple_list


def split_nodes_image(old_nodes):
    ret_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            ret_nodes.append(node)
            continue
            
        text = node.text
        list_of_links = extract_markdown_images(text)
        
        if len(list_of_links) == 0:
            ret_nodes.append(node)
            continue  # Add this!

        else:
            for link in list_of_links:
                split_text = f"![{link[0]}]({link[1]})"
                text_list = text.split(split_text, 1)

                if text_list[0]:
                    new_node = TextNode(text_list[0], TextType.TEXT)
                    ret_nodes.append(new_node)
                
                link_node = TextNode(link[0], TextType.IMAGE, link[1])
                ret_nodes.append(link_node)

                text = text_list[1]                
                
            if text:
                new_node = TextNode(text, TextType.TEXT)
                ret_nodes.append(new_node)
    
    return ret_nodes

def split_nodes_link(old_nodes):
    ret_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            ret_nodes.append(node)
            continue
            
        text = node.text
        list_of_links = extract_markdown_links(text)

        if len(list_of_links) == 0:
            ret_nodes.append(node)
            continue  # Add this!

        else:  # Add this!
            for link in list_of_links:
                split_text =  f"[{link[0]}]({link[1]})"
                text_list = text.split(split_text, 1)

                if text_list[0]:
                    new_node = TextNode(text_list[0], TextType.TEXT)
                    ret_nodes.append(new_node)

                link_node = TextNode(link[0], TextType.LINK, link[1])
                ret_nodes.append(link_node)
                
                text = text_list[1]

            if text:
                new_node = TextNode(text, TextType.TEXT)
                ret_nodes.append(new_node)
    
    return ret_nodes


def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes


def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    blocks = list(map(lambda x : x.strip(), blocks))
    blocks = list(filter(lambda x : len(x) > 0, blocks))
    return blocks

