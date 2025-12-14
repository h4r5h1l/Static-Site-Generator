Markdown → HTML: Architecture Overview
This project converts a raw Markdown string into an HTML string in several clear stages. The goal is to separate responsibilities so the code is easy to follow and extend.

1. Core Data Types
   TextNode

Represents a piece of inline content with a type:
text, bold, italic, code, link, image, etc.
May store extra data for some types (e.g. URL for links, src/alt for images).
Still “Markdown-flavored”, not yet HTML.
HTMLNode (with ParentNode and LeafNode)

Represents an HTML element:
tag (e.g. "p", "h1", "a", "ul", "li", "code").
optional value for text content.
props for attributes (href, src, alt, …).
children for nested HTMLNodes.
to_html() renders the entire subtree to an HTML string. 2. Block-Level Processing
These functions work on large chunks of Markdown, like paragraphs, headings, lists, and code blocks.

Split document into blocks

blocks = markdown_to_blocks(markdown)

Input: full Markdown document as a single string.
Output: list of block strings, usually separated by blank lines.
Classify each block

block_type = block_to_blocktype(block)

Determines if a block is:
heading, paragraph, code block, quote, unordered list, ordered list, etc.
Uses patterns like:

# / ## / ### at the start → heading.

> at start of lines → quote.
> -, \*, or 1. / 2. etc. → lists.
> Convert each block to a block-level HTMLNode

Inside markdown_to_html_node(markdown):

For each block:
Compute block_type.
Strip block-level markers:
headings: remove leading #....
lists: remove - , \* , or 1. , etc.
quotes: remove > .
code blocks: remove ``` fences.
For most block types, take the inner text and pass it to the inline parser via text_to_children (see below).
Wrap the resulting inline nodes in a block-level element:
heading → <h1>–<h6>
paragraph → <p>
unordered list → <ul><li>…</li></ul>
ordered list → <ol><li>…</li></ol>
quote → <blockquote>…</blockquote>
code block → <pre><code>…</code></pre> (special case, no inline parsing)
Build the root div

root = ParentNode(tag="div", children=all_block_nodes)

The entire document is represented as a single <div> whose children are the block nodes. 3. Inline Processing (Inside Blocks)
Inline processing turns text like **bold**, _italic_, `code`, [link](url), and ![alt](src) into structured nodes.

text_to_children(text: str) -> list[HTMLNode]

High-level role: str (markdown) → TextNodes → inline HTMLNodes.

Typical flow:

def text_to_children(text: str) -> list[HTMLNode]: # Start with a single plain TextNode
text_nodes = [TextNode(text, text_type_text)]

    # Run through inline parsers (each returns new TextNodes)
    text_nodes = split_nodes_delimiter(text_nodes, "**", text_type_bold)
    text_nodes = split_nodes_delimiter(text_nodes, "*", text_type_italic)
    text_nodes = split_nodes_delimiter(text_nodes, "`", text_type_code)

    text_nodes = split_nodes_image(text_nodes)  # ![alt](src)
    text_nodes = split_nodes_link(text_nodes)   # [text](url)

    # Convert TextNodes to HTMLNodes
    html_children = [text_node_to_html_node(tn) for tn in text_nodes]
    return html_children

Inline splitters (split*nodes*\*)

Work on a list of TextNodes.
Look for specific patterns and split/change node types:
split*nodes_delimiter handles bold/italic/inline code delimited by \**, *, *, `.
split_nodes_image finds ![alt](src) and creates image TextNodes.
split_nodes_link finds [text](url) and creates link TextNodes.
text_node_to_html_node(text_node: TextNode) -> HTMLNode

Bridges TextNode to HTMLNode:
if tn.text_type == text_type_text:
return LeafNode(tag=None, value=tn.text)
if tn.text_type == text_type_bold:
return LeafNode(tag="b", value=tn.text)
if tn.text_type == text_type_italic:
return LeafNode(tag="i", value=tn.text)
if tn.text_type == text_type_code:
return LeafNode(tag="code", value=tn.text)
if tn.text_type == text_type_link:
return LeafNode(tag="a", value=tn.text, props={"href": tn.url})
if tn.text_type == text_type_image:
return LeafNode(tag="img", value="", props={"src": tn.url, "alt": tn.text})

4. End-to-End Flow
   Putting it all together:

markdown (string)
markdown_to_blocks(markdown) → list of block strings
For each block:
block_to_blocktype(block)
Clean block syntax.
For most blocks: text_to_children(inner_text):
inner_text → TextNodes → inline HTMLNodes.
Wrap inline HTMLNodes in a block-level ParentNode (<p>, <h1>, <ul>, etc.).
For code blocks: build <pre><code>…</code></pre> directly without inline parsing.
Collect all block nodes under a root <div>.
Call root.to_html() to produce the final HTML string.
If you’d like, we can add a small diagram or comments inside markdown_to_html_node that reference these steps so someone reading the code can jump back to this overview
