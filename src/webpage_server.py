import os
import shutil
from .markdown_to_html import markdown_to_html

def cp_static_to_public(static_path, public_path):
        for dir_file in os.listdir(public_path):
            path = os.path.join(public_path, dir_file)
            try:
                if os.path.isfile(path):
                    os.remove(path)
                elif os.path.isdir(path):
                    shutil.rmtree(path)
            except Exception as e:
                print(f"Error removing {path}: {e}")
        for dir_file in os.listdir(static_path):
            src_path = os.path.join(static_path, dir_file)
            dest_path = os.path.join(public_path, dir_file)
            try:
                if os.path.isfile(src_path):
                    shutil.copy2(src_path, dest_path)
                    print(f"Copied {src_path} to {dest_path}")
                elif os.path.isdir(src_path):
                    shutil.copytree(src_path, dest_path)
                    print(f"Copied directory {src_path} to {dest_path}")
            except Exception as e:
                print(f"Error copying {src_path} to {dest_path}: {e}")
                

def extract_title(markdown):
    lines = markdown.splitlines()
    for line in lines:
        if line.startswith("# "):
            return line[2:].strip()
    raise ValueError("No title found in markdown")

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path}")
    with open(from_path, "r") as f:
        markdown = f.read()
        html_node = markdown_to_html(markdown)
        try:
            html = html_node.to_html()
        except AttributeError:
            html = str(html_node)
        title = extract_title(markdown)

    with open(template_path, "r") as f:
        template = f.read()
        page = template.replace("{{ Title }}", title).replace("{{ Content }}", html)

    # ensure destination directory exists
    dest_dir = os.path.dirname(dest_path)
    if dest_dir:
        os.makedirs(dest_dir, exist_ok=True)

    with open(dest_path, "w") as f:
        f.write(page)

    # Return the generated page HTML string so callers (and tests) can inspect it
    return page

def generate_pages_recursively(dir_path_content, template_path, dest_dir_path, return_map: bool = False):
    """Recursively generate pages from markdown files under `dir_path_content`.

    Args:
        dir_path_content: source content directory to walk
        template_path: path to the template file
        dest_dir_path: destination directory to write generated HTML files
        return_map: if True, return a dict mapping source_md_path -> dest_html_path
                    otherwise return a list of generated dest paths (backwards compatible)

    Returns:
        list[str] or dict: list of generated destination paths or mapping from source to dest
    """
    # ensure destination directory exists before writing files into it
    os.makedirs(dest_dir_path, exist_ok=True)
    generated = []
    mapping = {}
    for dir_file in os.listdir(dir_path_content):
        src_path = os.path.join(dir_path_content, dir_file)
        if dir_file.endswith(".md"):
            dest_path = os.path.join(dest_dir_path, dir_file.replace(".md", ".html"))
            # generate and record the output path
            generate_page(src_path, template_path, dest_path)
            generated.append(dest_path)
            mapping[src_path] = dest_path
        elif os.path.isdir(src_path):
            # recurse into subdirectory and collect generated files
            sub_generated = generate_pages_recursively(src_path, template_path, os.path.join(dest_dir_path, dir_file), return_map=return_map)
            if return_map:
                # sub_generated is a mapping
                mapping.update(sub_generated)
            else:
                generated.extend(sub_generated)
    return mapping if return_map else generated