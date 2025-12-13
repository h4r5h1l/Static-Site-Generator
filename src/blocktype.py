from enum import Enum

class BlockType(Enum):
    HEADING = "heading"
    PARAGRAPH = "paragraph"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"
    CODE = "code"
    QUOTE = "quote"


def block_to_blocktype(block: str) -> BlockType:
    if block.startswith("#"):
        return BlockType.HEADING
    if all(line.strip().startswith("- ") for line in block.splitlines()):
        return BlockType.UNORDERED_LIST
    if all(line.strip().startswith(f"{i+1}. ") for i, line in enumerate(block.splitlines())):
        return BlockType.ORDERED_LIST
    if block.startswith("```"):
        return BlockType.CODE
    if all(line.strip().startswith(">") for line in block.splitlines()):
        return BlockType.QUOTE
    return BlockType.PARAGRAPH


if __name__ == "__main__":
    heading_block = "# This is a heading"
    unordered_list_block = "- Item 1\n- Item 2\n- Item 3"
    paragraph_block = "This is a simple paragraph of text."
    ordered_list_block = "1. First item\n2. Second item\n3. Third item"
    code_block = "```\ndef hello_world():\n    print('Hello, world!')\n```"
    quote_block = "> This is a quote.\n> It spans multiple lines."
    block_type = block_to_blocktype(heading_block)
    print(f"The block type is: {block_type}")
    block_type = block_to_blocktype(unordered_list_block)
    print(f"The block type is: {block_type}")
    block_type = block_to_blocktype(paragraph_block)
    print(f"The block type is: {block_type}")
    block_type = block_to_blocktype(ordered_list_block)
    print(f"The block type is: {block_type}")
    block_type = block_to_blocktype(code_block)
    print(f"The block type is: {block_type}")
    block_type = block_to_blocktype(quote_block)
    print(f"The block type is: {block_type}")