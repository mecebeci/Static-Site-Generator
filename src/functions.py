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
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        split_nodes = []
        sections = old_node.text.split(delimiter)
        if len(sections) % 2 == 0:
            raise ValueError("invalid markdown, formatted section not closed")
        for i in range(len(sections)):
            if sections[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i], TextType.TEXT))
            else:
                split_nodes.append(TextNode(sections[i], text_type))
        new_nodes.extend(split_nodes)
    return new_nodes
            

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
            continue  

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
            continue  

        else:  
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


def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    ret_nodes = []
    for node in text_nodes:
        ret_nodes.append(text_node_to_html_node(node))
    return ret_nodes


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    main_child_nodes = []

    for block in blocks:
        block = block.strip()
        parser = MarkdownParser()
        type = parser.block_to_block_type(block)
        node = None

        match type:
            case BlockType.HEADING:
                heading_count = len(block) - len(block.lstrip("#"))
                heading_text = block.lstrip("#").strip()
                child_nodes = text_to_children(heading_text)
                node = ParentNode(f"h{heading_count}", child_nodes, None)

            case BlockType.CODE:
                lines = block.splitlines()
                code_lines = lines[1:-1]
                code_text = "\n".join(line.strip() for line in code_lines) + "\n"
                node = ParentNode("pre", [LeafNode("code", code_text, None)], None)

            case BlockType.QUOTE:
                lines = block.splitlines()
                quote_lines = []
                for line in lines:
                    line_without_gt = line[1:]
                    quote_lines.append(line_without_gt.strip())
                quote_text = " ".join(quote_lines)
                child_nodes = text_to_children(quote_text)
                node = ParentNode("blockquote", child_nodes, None)
                
            case BlockType.PARAGRAPH:
                paragraph_text = " ".join(line.strip() for line in block.splitlines())
                child_nodes = text_to_children(paragraph_text)
                node = ParentNode("p", child_nodes, None)

            case BlockType.UNORDERED_LIST:
                lines = block.splitlines()
                list_lines = []
                for line in lines:
                    line_without_dash = line[1:]
                    list_lines.append(line_without_dash.strip())
                
                list_of_li_nodes = []
                for line in list_lines:
                    child_nodes = text_to_children(line)
                    list_of_li_nodes.append(ParentNode("li", child_nodes))
                
                node = ParentNode("ul", list_of_li_nodes, None)

            case BlockType.ORDERED_LIST:
                lines = block.splitlines()
                list_lines = []
                for line in lines:
                    pattern = r'^\d+\.\s+(.*)$'
                    match = re.match(pattern, line.strip())
                    if match:
                        list_lines.append(match.group(1))

                list_of_li_nodes = []
                for line in list_lines:
                    child_nodes = text_to_children(line)
                    list_of_li_nodes.append(ParentNode("li", child_nodes))
                
                node = ParentNode("ol",  list_of_li_nodes, None)

        main_child_nodes.append(node)

    return ParentNode("div",  main_child_nodes, None)    
        