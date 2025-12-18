# Markdown → HTML: Architecture Overview

This project converts Markdown into HTML using a small, well-separated pipeline so each responsibility is easy to understand and extend.

## 1. Core data types

- **TextNode** — represents inline content (e.g., text, bold, italic, code, link, image). Some types carry extra data (URL for links, src/alt for images). TextNodes are still Markdown-flavored — not HTML yet.

- **HtmlNode** — abstract node representing HTML elements. Two main subclasses:
  - **ParentNode** — container nodes with a `tag` (e.g., `div`, `p`, `ul`) and `children`.
  - **LeafNode** — leaf nodes that have a `tag` (or `None` for plain text) and a `value` for text content, plus optional `props` (attributes like `href` or `src`).

Both node types implement `to_html()` to render the subtree to a string.

## 2. Block-level processing

Block-level functions operate on larger chunks of the document (paragraphs, headings, lists, code blocks).

### Splitting into blocks

Use `markdown_to_blocks(markdown)` to split the document into block strings (usually separated by blank lines).

### Classifying blocks

Use `block_to_blocktype(block)` to classify blocks such as: heading, paragraph, code block, quote, unordered list, ordered list.

Patterns used include:

- Headings: lines that start with `#` (one or more)
- Quotes: lines that start with `>`
- Lists: lines that start with `-`, `*`, or numeric enumerations like `1.`

### Converting blocks to `HtmlNode`

Inside `markdown_to_html_node(markdown)` each block is:

1. Classified (`block_type = block_to_blocktype(block)`).
2. Cleaned of block-level markers (e.g., remove leading `#` for headings or list markers for list items).
3. For most block types, the inner text is sent to the inline parser (`text_to_children`) and its resulting children are wrapped in a block-level `ParentNode`:

- Heading → `<h1>`–`<h6>`
- Paragraph → `<p>`
- Unordered list → `<ul><li>…</li></ul>`
- Ordered list → `<ol><li>…</li></ol>`
- Quote → `<blockquote>…</blockquote>`
- Code block → `<pre><code>…</code></pre>` (special case: no inline parsing)

The whole document is represented as a root `ParentNode(tag="div")` whose children are the block nodes.

## 3. Inline processing

Inline processing converts constructs like `**bold**`, `_italic_`, `` `code` ``, `[link](url)`, and `![alt](src)` into structured nodes.

### `text_to_children(text: str) -> list[HtmlNode]`

Typical flow:

```py
# Start with a single plain TextNode
text_nodes = [TextNode(text, TextType.TEXT)]

# Run inline splitters (each returns a new list of TextNodes)
text_nodes = split_nodes_delimiter(text_nodes, "**", TextType.BOLD)
text_nodes = split_nodes_delimiter(text_nodes, "_", TextType.ITALIC)
text_nodes = split_nodes_delimiter(text_nodes, "`", TextType.CODE)

text_nodes = split_nodes_image(text_nodes)  # ![alt](src)
text_nodes = split_nodes_link(text_nodes)   # [text](url)

# Convert TextNodes to HtmlNodes
html_children = [TextNode.text_node_to_html_node(tn) for tn in text_nodes]
```

### Inline splitters

- `split_nodes_delimiter` handles emphasis/strong/code markers.
- `split_nodes_image` detects `![alt](src)` and creates image nodes.
- `split_nodes_link` detects `[text](url)` and creates link nodes.

### TextNode → HtmlNode mapping

- Plain text → `LeafNode(tag=None, value=...)`
- Bold → `LeafNode(tag="b", value=...)`
- Italic → `LeafNode(tag="i", value=...)`
- Inline code → `LeafNode(tag="code", value=...)`
- Link → `LeafNode(tag="a", value=..., props={"href": url})`
- Image → `LeafNode(tag="img", props={"src": url, "alt": alt})` (renders as a void/self-closing tag)

## 4. End-to-end flow

1. `markdown_to_blocks(markdown)` → list of block strings
2. For each block:
   - classify (`block_to_blocktype`) and clean syntax
   - convert to inline nodes with `text_to_children` (unless it’s a code block)
   - wrap inline nodes in a block-level `ParentNode` (`p`, `h1` etc.)
3. Collect all block nodes under a root `<div>` (`ParentNode(tag="div")`)
4. Call `root.to_html()` to produce the final HTML string

## Running & testing

Run the unit tests:

```bash
bash test.sh
```

Run the site script (it checks port 8888 before starting):

```bash
bash main.sh
# or run the module directly
python3 -m src.main
```

If port 8888 is in use, `main.sh` will print an explanatory message and exit. Use `ps -ef | grep http.server` to find and stop an existing server.

---

## Diagram

Mermaid flowchart (GitHub supports Mermaid diagrams in READMEs):

```mermaid
flowchart LR
  MD[Markdown text] --> Blocks[markdown_to_blocks]
  Blocks --> BlockType[block_to_blocktype]
  BlockType --> Inline[text_to_children]
  Inline --> HtmlNodes[HtmlNode (Parent/Leaf)]
  HtmlNodes --> Root[ParentNode(div)]
  Root --> HTML["root.to_html() → HTML string"]
```

ASCII fallback:

```
Markdown text
  |
  v
blocks (markdown_to_blocks)
  |
  v
classify (block_to_blocktype)
  |
  v
inline parsing (text_to_children) -> HtmlNodes
  |
  v
root ParentNode(div)
  |
  v
root.to_html() -> final HTML string
```
