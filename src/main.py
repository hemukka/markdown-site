import os
import sys
import shutil
from re import findall

from markdown_html import markdown_to_html_node

def copy_static_files(dir="static", cur_path=""):
    lsd = os.listdir(dir)
    #print(lsd)

    for item in lsd:
        src = os.path.join(dir, item)
        dst = os.path.join("docs", cur_path, item)
        if os.path.isfile(src):
            print(f"{src} -> {dst}")
            shutil.copy(src, dst)
        else:
            os.mkdir(dst)
            #print(f"-> {src}")
            copy_static_files(src, os.path.join(cur_path, item))


def extract_title(markdown):
    title = findall(r"(?m)^# (.*)", markdown)
    if len(title) == 0:
        raise Exception("no h1 header for title")
    return title[0]


def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path) as file:
        markdown = file.read()
    with open(template_path) as file:
        template = file.read()
    
    content = markdown_to_html_node(markdown).to_html()
    #content = "test"
    title = extract_title(markdown)

    html = template.replace("{{ Title }}", title)
    html = html.replace("{{ Content }}", content)
    html = html.replace('href="/', f'href="{basepath}')
    html = html.replace('src="/', f'src="{basepath}')

    if not os.path.exists(os.path.dirname(dest_path)):
        os.makedirs(os.path.dirname(dest_path))

    with open(dest_path, 'w') as file:
        file.write(html)
    

def generate_pages_recursively(dir_path_content, template_path, dest_dir_path, basepath):
    for item in os.listdir(dir_path_content):
        content_path = os.path.join(dir_path_content, item)
        dest_path = os.path.join(dest_dir_path, item)
        if os.path.isfile(content_path):
            generate_page(content_path, template_path, dest_path.replace(".md", ".html"), basepath)
        else:
            os.mkdir(dest_path)
            generate_pages_recursively(content_path, template_path, dest_path, basepath)

def main():
    if len(sys.argv) < 2:
        basepath = "/"
    else:
        basepath = sys.argv[1]
        
    
    if os.path.exists("public"):
        shutil.rmtree("public")
    if os.path.exists("docs"):
        shutil.rmtree("docs")
    os.mkdir("docs")
    copy_static_files()
    generate_pages_recursively("content", "template.html", "docs", basepath)

if __name__ == "__main__":
    main()
