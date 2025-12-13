from textnode import *
from blocktype import BlockType, block_to_blocktype
from htmlnode import *

import re

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

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    return [block.strip() for block in blocks if block.strip()]

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = [TextNode.text_node_to_html_node(tn) for tn in text_nodes]
    return children

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    html_nodes = []
    for block in blocks:
        block_type = block_to_blocktype(block)
        if block_type == BlockType.HEADING:
            count = len(re.match(r"^#+", block).group())
            tag = f"h{count}"
            value = block[count:].strip()
            children = text_to_children(value)
            html_nodes.append(ParentNode(tag=tag, children=children))
        elif block_type == BlockType.PARAGRAPH:
            children = text_to_children(block)
            html_nodes.append(ParentNode(tag="p", children=children))
        elif block_type == BlockType.UNORDERED_LIST:
            list_items = block.splitlines()
            li_nodes = []
            for item in list_items:
                item_text = item.lstrip("- ").strip()
                item_children = text_to_children(item_text)
                li_nodes.append(ParentNode(tag="li", children=item_children))
            html_nodes.append(ParentNode(tag="ul", children=li_nodes))
        elif block_type == BlockType.ORDERED_LIST:
            list_items = block.splitlines()
            li_nodes = []
            for item in list_items:
                item_text = re.sub(r"^\d+\.\s+", "", item).strip()
                item_children = text_to_children(item_text)
                li_nodes.append(ParentNode(tag="li", children=item_children))
            html_nodes.append(ParentNode(tag="ol", children=li_nodes))
        elif block_type == BlockType.CODE:
            code_content = "\n".join(block.splitlines()[1:-1])
            code_node = LeafNode(tag="code", value=code_content)
            html_nodes.append(ParentNode(tag="pre", children=[code_node]))

        elif block_type == BlockType.QUOTE:
            quote_lines = block.splitlines()
            quote_text = "\n".join(line.lstrip("> ").strip() for line in quote_lines)
            children = text_to_children(quote_text)
            html_nodes.append(ParentNode(tag="blockquote", children=children))
    return ParentNode(tag="div", children=html_nodes, props={})

                
if __name__ == "__main__":
    markdown = "# This is a heading\n\n       \n\n    This is a paragraph of text. It has some **bold** and _italic_ words inside of it.\n\n- This is the first list item in a list block\n- This is a list item\n- This is another list item"

    html_tree = markdown_to_html_node(markdown)
    print(html_tree.to_html())