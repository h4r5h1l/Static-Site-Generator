from leafnode import LeafNode
import unittest

class TestLeafNode(unittest.TestCase):
    def test_to_html_with_tag_and_value(self):
        node = LeafNode(tag="p", value="Hello, World!")
        self.assertEqual(node.to_html(), "<p>Hello, World!</p>")

    def test_to_html_with_value_only(self):
        node = LeafNode(value="Just text")
        self.assertEqual(node.to_html(), "Just text")

    def test_to_html_with_tag_value_and_props(self):
        node = LeafNode(tag="a", value="Click here", props={"href": "http://example.com"})
        self.assertEqual(node.to_html(), '<a href="http://example.com">Click here</a>')

    def test_to_html_without_value_raises_error(self):
        node = LeafNode(tag="p")
        with self.assertRaises(ValueError):
            node.to_html()

    def test_repr(self):
        node = LeafNode(tag="span", value="Text", props={"class": "highlight"})
        self.assertEqual(repr(node), "LeafNode(tag=span, value=Text, props={'class': 'highlight'})")
        
if __name__ == "__main__":
    unittest.main()