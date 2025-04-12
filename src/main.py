import os
import shutil

from textnode import TextNode, TextType
from htmlnode import LeafNode

def copy_static_files(dir="static/"):
    pass


def main():
    
    shutil.rmtree("public/")
    copy_static_files()

if __name__ == "__main__":
    main()
