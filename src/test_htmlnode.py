import unittest
from htmlnode import HtmlNode
from textnode import TextNode, TextType

class TestHtmlNode(unittest.TestCase):
    def test_initialization(self):
        node = HtmlNode(tag="div", value="Hello", children=[], props={"class": "my-class"})
        self.assertEqual(node.tag, "div")
        self.assertEqual(node.value, "Hello")
        self.assertEqual(node.children, [])
        self.assertEqual(node.props, {"class": "my-class"})

    def test_props_to_html(self):
        node = HtmlNode(props={"class": "my-class", "id": "my-id"})
        props_html = node.props_to_html()
        self.assertIn('class="my-class"', props_html)
        self.assertIn('id="my-id"', props_html)
        
    def test_repr(self):
        node = HtmlNode(tag="p", value="Paragraph")
        repr_str = repr(node)
        self.assertIn("HtmlNode", repr_str)

    def test_text_node_to_html_node(self):
        
        text_node_plain = TextNode("Hello", TextType.TEXT)
        self.assertEqual(HtmlNode.text_node_to_html_node(text_node_plain), "Hello")
        
        text_node_link = TextNode("Click here", TextType.LINK, "https://example.com")
        self.assertEqual(HtmlNode.text_node_to_html_node(text_node_link), '<a href="https://example.com">Click here</a>')
        
        text_node_bold = TextNode("Bold Text", TextType.BOLD)
        self.assertEqual(HtmlNode.text_node_to_html_node(text_node_bold), '<strong>Bold Text</strong>')
        
        text_node_italic = TextNode("Italic Text", TextType.ITALIC)
        self.assertEqual(HtmlNode.text_node_to_html_node(text_node_italic), '<em>Italic Text</em>')
        
        text_node_code = TextNode("Code Snippet", TextType.CODE)
        self.assertEqual(HtmlNode.text_node_to_html_node(text_node_code), '<code>Code Snippet</code>')
        
        text_node_image = TextNode("Image Alt", TextType.IMAGE, "https://example.com/image.png")
        self.assertEqual(HtmlNode.text_node_to_html_node(text_node_image), '<img src="https://example.com/image.png" alt="Image Alt"/>')

if __name__ == "__main__":
    unittest.main()