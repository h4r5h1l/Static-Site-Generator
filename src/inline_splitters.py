import re
from src.textnode import *
def split_nodes_delimeter(old_nodes, delimeter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        if node.text.count(delimeter) % 2 != 0:
            raise ValueError("Invalid markdown syntax: unmatched delimeters")
        parts = node.text.split(delimeter)
        for i, part in enumerate(parts):
            if part == "":
                continue
            if i % 2 == 0:
                new_nodes.append(TextNode(part, TextType.TEXT))
            else:
                new_nodes.append(TextNode(part, text_type))
    return new_nodes

def extract_markdown_links(text):
    # Only match links, not images
    link_pattern = r"(?<!!)\[([^\[\]]+)\]\(([^\(\)]+)\)"
    return re.findall(link_pattern, text)

def extract_markdown_images(text):
    img_pattern = r"!\[([^\[\]]+)\]\(([^\(\)]+)\)"
    return re.findall(img_pattern, text)

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        images = extract_markdown_images(node.text)
        if not images:
            new_nodes.append(node)
            continue
        for image_text, image_url in images:
            parts = node.text.split(f"![{image_text}]({image_url})", 1)
            if parts[0]:
                new_nodes.append(TextNode(parts[0], TextType.TEXT))
            new_nodes.append(TextNode(image_text, TextType.IMAGE, image_url))
            text = parts[1]
            if text:
                new_nodes.append(TextNode(text, TextType.TEXT))    
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        links = extract_markdown_links(node.text)
        if not links:
            new_nodes.append(node)
            continue
        for link_text, link_url in links:
            parts = node.text.split(f"[{link_text}]({link_url})", 1)
            if parts[0]:
                new_nodes.append(TextNode(parts[0], TextType.TEXT))
            new_nodes.append(TextNode(link_text, TextType.LINK, link_url))
            text = parts[1]
            if text:
                new_nodes.append(TextNode(text, TextType.TEXT))
    return new_nodes
def text_to_textnodes(text):
    new_nodes = [TextNode(text, TextType.TEXT)]
    delimiter_texttype = [
        ("**", TextType.BOLD),
        ("_", TextType.ITALIC),
        ("`", TextType.CODE)
    ]
    for delimiter, text_type in delimiter_texttype:
        new_nodes = split_nodes_delimeter(new_nodes, delimiter, text_type)
    new_nodes = split_nodes_image(new_nodes)
    new_nodes = split_nodes_link(new_nodes)
    return new_nodes