"""markdown_to_html

High level overview:
- Split markdown text into blocks (markdown_to_blocks)
- Classify each block (block_to_blocktype)
- Convert block contents to inline HTML nodes (text_to_children)
- Wrap inline children in block-level ParentNodes
- Return a root ParentNode(tag="div") for the whole document

This module contains the functions used to map markdown -> HtmlNode tree.
"""

from .textnode import *
from .blocktype import *
from .htmlnode import *
from .inline_splitters import *
import re

def markdown_to_blocks(markdown):
    """Split a markdown document into non-empty blocks.

    Blocks are typically separated by one or more blank lines. The function
    returns a list of cleaned, stripped block strings.
    """
    blocks = markdown.split("\n\n")
    return [block.strip() for block in blocks if block.strip()]

def text_to_children(text):
    """Convert a markdown inline text into HtmlNode children.

    The function runs inline splitters to produce a list of TextNodes and then
    converts those to HtmlNodes (LeafNodes / images / links) that are suitable
    to be children of a ParentNode.
    """
    # str (markdown) -> [TextNode] (inline parse) -> [LeafNode] (inline HTML)
    text_nodes = text_to_textnodes(text)
    children = [TextNode.text_node_to_html_node(tn) for tn in text_nodes]
    return children

def markdown_to_html(markdown):
    """Parse a whole markdown document into a tree of HtmlNodes.

    Returns:
        ParentNode: root div node containing block-level children.

    Notes:
    - Headings, paragraphs, lists, quotes, and code blocks are supported.
    - Inline parsing is delegated to `text_to_children` for most block types.
    """
    all_nodes = []
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        # decide the block type and build appropriate HtmlNodes
        block_type = block_to_blocktype(block)
        if block_type == BlockType.HEADING:
            # heading level determined by leading # characters
            hash_count = len(re.match(r"^#+", block).group())
            children = text_to_children(block[hash_count:].strip())
            all_nodes.append(ParentNode(tag=f"h{hash_count}", children=children))
        elif block_type == BlockType.PARAGRAPH:
            # paragraphs are inline-parsed
            children = text_to_children(block)
            all_nodes.append(ParentNode(tag="p", children=children))
        elif block_type == BlockType.UNORDERED_LIST:
            # list items are split by lines and each item is inline-parsed
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
            # code fences preserve their inner text verbatim
            code_content = "\n".join(block.splitlines()[1:-1])
            code_node = LeafNode(tag="code", value=code_content)
            all_nodes.append(ParentNode(tag="pre", children=[code_node]))

        elif block_type == BlockType.QUOTE:
            # strip leading > markers and inline-parse the result
            quote_lines = block.splitlines()
            quote_text = "\n".join(line.lstrip("> ").strip() for line in quote_lines)
            children = text_to_children(quote_text)
            all_nodes.append(ParentNode(tag="blockquote", children=children))

    return ParentNode(tag="div", children=all_nodes, props={})


                
if __name__ == "__main__":
    markdown = "# This is a heading\n\n       \n\n    This is a paragraph of text. It has some **bold** and _italic_ words inside of it.\n\n- This is the first list item in a list block\n- This is a list item\n- This is another list item"
    print(markdown_to_html(markdown))