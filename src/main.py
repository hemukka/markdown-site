import os
import sys
import shutil
from re import findall

from markdown_html import markdown_to_html_node


def copy_static_files(from_dir_path, dest_dir_path):
    """ Copy everything from_dir_path to dest_dir_path. """
    for item in os.listdir(from_dir_path):
        src = os.path.join(from_dir_path, item)
        dst = os.path.join(dest_dir_path, item)
        if os.path.isfile(src):
            print(f"Copying file: {src} -> {dst}")
            shutil.copy(src, dst)
        else:
            #print(f"-> {src}")
            os.mkdir(dst)
            copy_static_files(src, dst)


def extract_title(markdown):
    """ Return text of the first h1 level heading (#). """
    title = findall(r"(?m)^# (.*)", markdown)
    if len(title) == 0:
        raise Exception("no h1 header for title")
    return title[0]


def generate_page(from_path, template_path, dest_path, basepath):
    """ Convert markdown file in from_path to html file in dest_path. """
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
    """ Call generate_content on all files in dir_path_content. """
    for item in os.listdir(dir_path_content):
        content_path = os.path.join(dir_path_content, item)
        dest_path = os.path.join(dest_dir_path, item)
        if os.path.isfile(content_path):
            if content_path.endswith(".md"):
                generate_page(content_path,
                              template_path,
                              dest_path.replace(".md", ".html"),
                              basepath)
            else:
                print(f"Skipping non-markdown file: {content_path}")
        else:
            os.mkdir(dest_path)
            generate_pages_recursively(content_path, template_path, dest_path, basepath)


dir_path_static = "static"
dir_path_public = "docs"
dir_path_content = "content"
template_path = "template.html"
default_basepath = "/"


def main():
    if len(sys.argv) < 2:
        basepath = default_basepath
    else:
        basepath = sys.argv[1]
    print(f"Site's root path set as: {basepath}")
    
    print("Clearing public directory...")
    if os.path.exists(dir_path_public):
        shutil.rmtree(dir_path_public)
    os.mkdir(dir_path_public)

    print("Copying static files to public directory...")
    copy_static_files(dir_path_static, dir_path_public)

    print("Generating content...")
    generate_pages_recursively(dir_path_content, template_path, dir_path_public, basepath)


if __name__ == "__main__":
    main()
