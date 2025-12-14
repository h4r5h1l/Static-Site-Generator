from src.textnode import *
from src.blocktype import *
from src.htmlnode import *
from src.inline_splitters import *
import re

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    return [block.strip() for block in blocks if block.strip()]

def text_to_children(text):
    #   str (markdown) -> [TextNode] (inline parse) -> [LeafNode] (inline HTML)
    text_nodes = text_to_textnodes(text)
    children = [TextNode.text_node_to_html_node(tn) for tn in text_nodes]
    return children

def markdown_to_html(markdown):
    all_nodes = []
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        block_type = block_to_blocktype(block)
        if block_type == BlockType.HEADING:
            hash_count = len(re.match(r"^#+", block).group())
            children = text_to_children(block[hash_count:].strip())
            all_nodes.append(ParentNode(tag=f"h{hash_count}", children=children))
        elif block_type == BlockType.PARAGRAPH:
            children = text_to_children(block)
            all_nodes.append(ParentNode(tag="p", children=children))
        elif block_type == BlockType.UNORDERED_LIST:
            list_items = block.splitlines()
            li_nodes = []
            for item in list_items:
                item_text = item.lstrip("- ").strip()
                item_children = text_to_children(item_text)
                li_nodes.append(ParentNode(tag="li", children=item_children))
            all_nodes.append(ParentNode(tag="ul", children=li_nodes))
        elif block_type == BlockType.ORDERED_LIST:
            list_items = block.splitlines()
            li_nodes = []
            for item in list_items:
                item_text = re.sub(r"^\d+\.\s+", "", item).strip()
                item_children = text_to_children(item_text)
                li_nodes.append(ParentNode(tag="li", children=item_children))
            all_nodes.append(ParentNode(tag="ol", children=li_nodes))
        elif block_type == BlockType.CODE:
            code_content = "\n".join(block.splitlines()[1:-1])
            code_node = LeafNode(tag="code", value=code_content)
            all_nodes.append(ParentNode(tag="pre", children=[code_node]))

        elif block_type == BlockType.QUOTE:
            quote_lines = block.splitlines()
            quote_text = "\n".join(line.lstrip("> ").strip() for line in quote_lines)
            children = text_to_children(quote_text)
            all_nodes.append(ParentNode(tag="blockquote", children=children))

    return ParentNode(tag="div", children=all_nodes, props={})


                
if __name__ == "__main__":
    markdown = "# This is a heading\n\n       \n\n    This is a paragraph of text. It has some **bold** and _italic_ words inside of it.\n\n- This is the first list item in a list block\n- This is a list item\n- This is another list item"
    print(markdown_to_html(markdown))