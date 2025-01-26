import os
import argparse
import shutil
from markdown_blocks import markdown_to_html_node

def main(public_dir, static_dir):
    pass
    #print(f"Public directory: {public_dir}")
    #print(f"Static directory: {static_dir}")
    #prepare_public(public_dir,static_dir)
    #print("copying static files!")
    #copy_content(public_dir,static_dir)


def prepare_public(public_dir,static_dir):
    if not os.path.exists(static_dir):
        raise ValueError("Static Path does not exist")
    if os.path.exists(public_dir):
        print("deleting old public files!")
        shutil.rmtree(public_dir)
    os.makedirs(public_dir)



def copy_content(public_dir,static_dir):
    print(os.listdir(static_dir))
    for item in os.listdir(static_dir):
        if os.path.isdir(static_dir + item):
            os.makedirs(public_dir + item + "/",exist_ok=True)
            copy_content(public_dir + item + "/",static_dir + item + "/")
        else:
            shutil.copy(static_dir + item,public_dir+item)


def extract_title(markdown):
    for line in markdown.split("\n"):
        if line.startswith("# "):
            return line[1:].strip().split()[0]

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    print(f"Generating files in directory {dir_path_content}")
    for item in os.listdir(dir_path_content):
        if item.endswith(".md"):
            print(dir_path_content)
            generate_page(dir_path_content + item ,template_path,dest_dir_path + item[:-3] + ".html")
        elif os.path.isdir(dir_path_content + item + "/"):
            os.makedirs(dest_dir_path + item + "/",exist_ok=True)
            print("generating recursively on " + dir_path_content + item + "/")
            generate_pages_recursive(dir_path_content + item + "/",template_path, dest_dir_path + item + "/")




def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path) as f:
        lines = f.read()
    with open(template_path) as f:
        template = f.read()
    htmllines = markdown_to_html_node(lines).to_html()
    template = template.replace('{{ Title }}', extract_title(lines))
    template = template.replace('{{ Content }}', htmllines)
    with open(dest_path,"w") as f:
        f.write(template)



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process two directories: public and static.")
    parser.add_argument("public_dir", type=str, help="Path to the public directory")
    parser.add_argument("static_dir", type=str, help="Path to the static directory")
    
    args = parser.parse_args()
    main(args.public_dir, args.static_dir)
