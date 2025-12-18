from src.markdown_to_html import *
import unittest

class TestMarkdownToHTML(unittest.TestCase):
    def test_markdown_to_blocks(self):
        markdown = "# This is a heading\n\n   \n    \n\n    This is a paragraph of text. It has some **bold** and _italic_ words inside of it.\n\n- This is the first list item in a list block\n- This is a list item\n- This is another list item"
        expected_blocks = [
            "# This is a heading",
            "This is a paragraph of text. It has some **bold** and _italic_ words inside of it.",
            "- This is the first list item in a list block\n- This is a list item\n- This is another list item"
        ]
        result = markdown_to_blocks(markdown)
        self.assertEqual(result, expected_blocks)

    def test_markdown_to_html(self):
        markdown = "# Heading\n\nThis is a **bold** text with a [link](https://example.com)."
        result = markdown_to_html(markdown)
        expected_html_nodes = [
            ParentNode(tag="h1", children=[
                LeafNode(tag=None, value="Heading", props={})
            ], props={}),
            ParentNode(tag="p", children=[
                LeafNode(tag=None, value="This is a ", props={}),
                LeafNode(tag="b", value="bold", props={}),
                LeafNode(tag=None, value=" text with a ", props={}),
                LeafNode(tag="a", value="link", props={"href": "https://example.com"})
            ,
                LeafNode(tag=None, value=".", props={})
            ], props={})
        ]
        self.assertEqual(result.children, expected_html_nodes) 
        
        
if __name__ == "__main__":
    unittest.main()