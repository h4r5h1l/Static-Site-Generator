from parentnode import ParentNode
from leafnode import LeafNode
import unittest

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
        
        
if __name__ == "__main__":
    unittest.main()