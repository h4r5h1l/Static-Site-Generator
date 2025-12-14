import unittest
from src.htmlnode import HtmlNode
from src.textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    node = TextNode("This is a text node", TextType.BOLD)
    node2 = TextNode("This is a text node", TextType.BOLD)
    node3 = TextNode("This is a different text node", TextType.ITALIC, url="https://example.com")

    def  test_eq(self):
        self.assertEqual(self.node, self.node2)
        
    def test_neq(self):
        self.assertNotEqual(self.node, self.node3)
        
    def test_none_url(self):
        self.assertIsNone(self.node.url)
        
    def test_eq_type(self):
        self.assertEqual(self.node.text_type, self.node2.text_type)
        
    def test_neq_type(self):
        self.assertNotEqual(self.node.text_type, self.node3.text_type)
        
    def test_text_node_to_html_node(self):
        
        text_node_plain = TextNode("Hello", TextType.TEXT)
        self.assertEqual(TextNode.text_node_to_html_node(text_node_plain), HtmlNode(tag=None, value="Hello", children=[], props={}))
        
        text_node_link = TextNode("Click here", TextType.LINK, "https://example.com")
        self.assertEqual(TextNode.text_node_to_html_node(text_node_link), HtmlNode(tag="a", value="Click here", children=[], props={"href": "https://example.com"}))
        
        text_node_bold = TextNode("Bold Text", TextType.BOLD)
        self.assertEqual(TextNode.text_node_to_html_node(text_node_bold), HtmlNode(tag="b", value="Bold Text", children=[], props={}))
        
        text_node_italic = TextNode("Italic Text", TextType.ITALIC)
        self.assertEqual(TextNode.text_node_to_html_node(text_node_italic), HtmlNode(tag="i", value="Italic Text", children=[], props={}))

        text_node_code = TextNode("Code Snippet", TextType.CODE)
        self.assertEqual(TextNode.text_node_to_html_node(text_node_code), HtmlNode(tag="code", value="Code Snippet", children=[], props={}))
        
        text_node_image = TextNode("Image Alt", TextType.IMAGE, "https://example.com/image.png")
        self.assertEqual(TextNode.text_node_to_html_node(text_node_image), HtmlNode(tag="img", value=None, children=[], props={"src": "https://example.com/image.png", "alt": "Image Alt"}))

if __name__ == "__main__":
    unittest.main()