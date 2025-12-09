import unittest
from htmlnode import HtmlNode

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


if __name__ == "__main__":
    unittest.main()