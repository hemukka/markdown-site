from enum import Enum
import re

class BlockType(Enum):
    P = "paragraph"
    H = "heading"
    CODE = "code"
    QUOTE = "quote"
    UL = "unordered_list"
    OL = "ordered_list"


def markdown_to_blocks(markdown: str) -> list[str]:
    blocks = markdown.split("\n\n")
    clean_blocks = []
    for block in blocks:
        block = block.strip()
        if block != "":
            clean_blocks.append(block)

    return clean_blocks


def block_to_block_type(block: str) -> BlockType:
    if re.match(r"#{1,6} .*", block):
        return BlockType.H
    elif re.fullmatch(r"^```[\s\S]*```$", block):
        return BlockType.CODE
    elif re.search(r"^>.*(\n>.*)*$", block):
        return BlockType.QUOTE
    elif re.search(r"^- .*(\n- .*)*$", block):
        return BlockType.UL
    elif is_ordered_list(block):
        return BlockType.OL
    else:
        return BlockType.P


# Check if block is an ordered list with proper incrementing
def is_ordered_list(block):
    lines = block.split('\n')
    
    for i, line in enumerate(lines):
        expected_prefix = f"{i+1}. "
        if not line.startswith(expected_prefix):
            return False
    
    return True