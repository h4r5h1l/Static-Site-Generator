from src.blocktype import BlockType, block_to_blocktype
import unittest

class TestBlockType(unittest.TestCase):
    def test_heading_block(self):
        block = "# This is a heading"
        expected_type = BlockType.HEADING
        result = block_to_blocktype(block)
        self.assertEqual(result, expected_type)

    def test_unordered_list_block(self):
        block = "- Item 1\n- Item 2\n- Item 3"
        expected_type = BlockType.UNORDERED_LIST
        result = block_to_blocktype(block)
        self.assertEqual(result, expected_type)

    def test_paragraph_block(self):
        block = "This is a simple paragraph of text."
        expected_type = BlockType.PARAGRAPH
        result = block_to_blocktype(block)
        self.assertEqual(result, expected_type)

    def test_ordered_list_block(self):
        block = "1. First item\n2. Second item\n3. Third item"
        expected_type = BlockType.ORDERED_LIST
        result = block_to_blocktype(block)
        self.assertEqual(result, expected_type)

    def test_code_block(self):
        block = "```\ndef hello_world():\n    print('Hello, world!')\n```"
        expected_type = BlockType.CODE
        result = block_to_blocktype(block)
        self.assertEqual(result, expected_type)

    def test_quote_block(self):
        block = "> This is a quote.\n> It spans multiple lines."
        expected_type = BlockType.QUOTE
        result = block_to_blocktype(block)
        self.assertEqual(result, expected_type)
        
if __name__ == "__main__":
    unittest.main()