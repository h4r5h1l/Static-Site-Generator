from markdown_to_textnode import split_node_delimeter
from textnode import TextNode, TextType 
import unittest

class TestMarkdownToTextNode(unittest.TestCase):
    def test_split_node_delimeter_bold(self):
        nodes = [TextNode("This is **bold** text", TextType.TEXT)]
        result = split_node_delimeter(nodes, "**", TextType.BOLD)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.TEXT)
        ]
        self.assertEqual(result, expected)

    def test_split_node_delimeter_italic(self):
        nodes = [TextNode("This is _italic_ text", TextType.TEXT)]
        result = split_node_delimeter(nodes, "_", TextType.ITALIC)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text", TextType.TEXT)
        ]
        self.assertEqual(result, expected)

    def test_split_node_delimeter_unmatched(self):
        nodes = [TextNode("This is **bold text", TextType.TEXT)]
        with self.assertRaises(ValueError):
            split_node_delimeter(nodes, "**", TextType.BOLD)
            
if __name__ == "__main__":
    unittest.main()