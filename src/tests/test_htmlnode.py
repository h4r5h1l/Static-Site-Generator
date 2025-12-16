import unittest
from src.htmlnode import HtmlNode, ParentNode, LeafNode
from src.textnode import TextNode, TextType

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


class TestParentNode(unittest.TestCase):
    def test_to_html_with_tag_and_children(self):
        child1 = LeafNode(tag="p", value="Child 1")
        child2 = LeafNode(tag="p", value="Child 2")
        parent = ParentNode(tag="div", children=[child1, child2])
        self.assertEqual(parent.to_html(), "<div><p>Child 1</p><p>Child 2</p></div>")

    def test_to_html_with_tag_children_and_props(self):
        child = LeafNode(tag="span", value="Hello")
        parent = ParentNode(tag="div", children=[child], props={"class": "container"})
        self.assertEqual(parent.to_html(), '<div class="container"><span>Hello</span></div>')

    def test_to_html_without_tag_raises_error(self):
        child = LeafNode(tag="p", value="Child")
        parent = ParentNode(children=[child])
        with self.assertRaises(ValueError):
            parent.to_html()

    def test_to_html_without_children_raises_error(self):
        parent = ParentNode(tag="div")
        with self.assertRaises(ValueError):
            parent.to_html()

    def test_repr(self):
        child = LeafNode(tag="p", value="Text")
        parent = ParentNode(tag="section", children=[child], props={"id": "main"})
        self.assertEqual(repr(parent), "ParentNode(tag=section, children=[LeafNode(tag=p, value=Text, props={})], props={'id': 'main'})")
        


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

        text_node_plain = TextNode("Hello", TextType.TEXT)
        node = TextNode.text_node_to_html_node(text_node_plain)
        result = node.to_html() if isinstance(node, HtmlNode) else str(node)
        self.assertEqual(result, "Hello")

        text_node_link = TextNode("Click here", TextType.LINK, "https://example.com")
        node = TextNode.text_node_to_html_node(text_node_link)
        result = node.to_html() if isinstance(node, HtmlNode) else str(node)
        self.assertEqual(result, '<a href="https://example.com">Click here</a>')

        text_node_bold = TextNode("Bold Text", TextType.BOLD)
        node = TextNode.text_node_to_html_node(text_node_bold)
        result = node.to_html() if isinstance(node, HtmlNode) else str(node)
        self.assertEqual(result, '<b>Bold Text</b>')

        text_node_italic = TextNode("Italic Text", TextType.ITALIC)
        node = TextNode.text_node_to_html_node(text_node_italic)
        result = node.to_html() if isinstance(node, HtmlNode) else str(node)
        self.assertEqual(result, '<i>Italic Text</i>')

        text_node_code = TextNode("Code Snippet", TextType.CODE)
        node = TextNode.text_node_to_html_node(text_node_code)
        result = node.to_html() if isinstance(node, HtmlNode) else str(node)
        self.assertEqual(result, '<code>Code Snippet</code>')

        text_node_image = TextNode("Image Alt", TextType.IMAGE, "https://example.com/image.png")
        node = TextNode.text_node_to_html_node(text_node_image)
        result = node.to_html() if isinstance(node, HtmlNode) else str(node)
        self.assertEqual(result, '<img src="https://example.com/image.png" alt="Image Alt"/>')

if __name__ == "__main__":
    unittest.main()