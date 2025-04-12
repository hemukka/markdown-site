import re

from textnode import TextType, TextNode

def text_to_textnodes(text: str):
    """ Return list of TextNodes (bold, italic, code, image, and link types) based on the input string. """
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes


def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType):
    """ Return a list of TextNodes created by splitting the old_nodes with the delimiter. """
    new_nodes = []
    for node in old_nodes:
        if  node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        split_text = node.text.split(delimiter)
        if len(split_text) % 2 == 0:
            raise Exception("invalid Markdown syntax, no closing delimiter")
        for i in range(len(split_text)):
            if split_text[i] == "":
                continue
            if i % 2 == 0:
                new_nodes.append(TextNode(split_text[i], TextType.TEXT))
            else:
                new_nodes.append(TextNode(split_text[i], text_type))
                
    return new_nodes

def split_nodes_image(old_nodes: list[TextNode]):
    """ Return a list of TextNodes created by splitting the old_nodes based on MD image syntax """
    new_nodes = []
    for node in old_nodes:
        if  node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        image_list = extract_markdown_images(node.text)
        if not image_list:
            new_nodes.append(node)
            continue

        remaining_text = node.text
        for alt_text, url in image_list:
            sections = remaining_text.split(f"![{alt_text}]({url})", maxsplit = 1)
            text_before = sections[0]
            remaining_text = sections[1]
            if text_before != "":
                new_nodes.append(TextNode(text_before, TextType.TEXT))
            new_nodes.append(TextNode(alt_text, TextType.IMAGE, url))
        
        if remaining_text != "":
            new_nodes.append(TextNode(remaining_text, TextType.TEXT))
                
    return new_nodes

def split_nodes_link(old_nodes: list[TextNode]):
    """ Return a list of TextNodes created by splitting the old_nodes based on MD link syntax """
    new_nodes = []
    for node in old_nodes:
        if  node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        link_list = extract_markdown_links(node.text)
        if not link_list:
            new_nodes.append(node)
            continue

        remaining_text = node.text
        for anchor_text, url in link_list:
            sections = remaining_text.split(f"[{anchor_text}]({url})", maxsplit = 1)
            text_before = sections[0]
            remaining_text = sections[1]
            if text_before != "":
                new_nodes.append(TextNode(text_before, TextType.TEXT))
            new_nodes.append(TextNode(anchor_text, TextType.LINK, url))
        
        if remaining_text != "":
            new_nodes.append(TextNode(remaining_text, TextType.TEXT))
                
    return new_nodes

def extract_markdown_images(text):
    return re.findall(r"!\[(.*?)\]\((.*?)\)", text)

def extract_markdown_links(text):
    return re.findall(r"\[(.*?)\]\((.*?)\)", text)