import unittest

from textnode import TextNode, TextType


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
        


if __name__ == "__main__":
    unittest.main()