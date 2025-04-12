from block_markdown import BlockType, markdown_to_blocks, block_to_block_type
from inline_markdown import text_to_textnodes
from textnode import text_node_to_html_node
from htmlnode import HTMLNode, ParentNode, LeafNode


def markdown_to_html_node(markdown: str) -> HTMLNode:
    blocks = []
    for block in markdown_to_blocks(markdown):
        block_type = block_to_block_type(block)
        match block_type:
            case BlockType.P:
                # remove newlines from paragraph text for now, should it be <br>?
                block = block.replace("\n", " ")
                blocks.append(ParentNode("p", text_to_children(block)))
            case BlockType.H:
                blocks.append(ParentNode(get_heading_tag(block),
                                         text_to_children(block.lstrip("# "))))
            case BlockType.CODE:
                blocks.append(ParentNode("pre", [LeafNode("code", block.strip("`\n"))]))
            case BlockType.QUOTE:
                new_block = ""
                for line in block.split("\n"):
                    new_block += line.lstrip("> ") + "\n"
                blocks.append(ParentNode("blockquote", text_to_children(new_block)))
            case BlockType.UL:
                list_items = []
                for line in block.split("\n"):
                    line = line.lstrip("- ")
                    list_items.append(ParentNode("li", text_to_children(line)))
                blocks.append(ParentNode("ul", list_items))
            case BlockType.OL:
                list_items = []
                i = 1
                for line in block.split("\n"):
                    line = line.lstrip(f"{i}. ")
                    i += 1
                    list_items.append(ParentNode("li", text_to_children(line)))
                blocks.append(ParentNode("ol", list_items))
            case _:
                raise Exception("undefined block type")

    return ParentNode("div", blocks)


def text_to_children(text):
    textnodes = text_to_textnodes(text)
    children = []
    for node in textnodes:
        children.append(text_node_to_html_node(node))
    return children

def get_heading_tag(text):
    for i in range(6):
        if text.startswith(f"{'#' * (i+1)} "):
            return f"h{i+1}"
    raise Exception("Heading improperly formatted.")