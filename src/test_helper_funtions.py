from helper_functions import split_nodes_delimeter, extract_markdown_links, extract_markdown_images, split_nodes_image, split_nodes_link, text_to_textnodes
import unittest
from textnode import TextNode, TextType

class TestHelperFunctions(unittest.TestCase):
    def test_split_nodes_delimeter_bold(self):
        old_nodes = [TextNode("This is **bold** text", TextType.TEXT)]
        expected_nodes = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.TEXT)
        ]
        result = split_nodes_delimeter(old_nodes, "**", TextType.BOLD)
        self.assertEqual(result, expected_nodes)

    def test_split_nodes_delimeter_italic(self):
        old_nodes = [TextNode("This is _italic_ text", TextType.TEXT)]
        expected_nodes = [
            TextNode("This is ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text", TextType.TEXT)
        ]
        result = split_nodes_delimeter(old_nodes, "_", TextType.ITALIC)
        self.assertEqual(result, expected_nodes)

    def test_split_nodes_delimeter_unmatched(self):
        old_nodes = [TextNode("This is **bold text", TextType.TEXT)]
        with self.assertRaises(ValueError):
            split_nodes_delimeter(old_nodes, "**", TextType.BOLD)

    def test_split_nodes_delimeter_no_delimiter(self):
        old_nodes = [TextNode("This is plain text", TextType.TEXT)]
        expected_nodes = [TextNode("This is plain text", TextType.TEXT)]
        result = split_nodes_delimeter(old_nodes, "**", TextType.BOLD)
        self.assertEqual(result, expected_nodes)
        
    def test_extract_markdown_links(self):
        text = "This is a [link](https://example.com) and an ![image](https://example.com/image.png)."
        expected_links = [
            ("link", "https://example.com")
        ]
        result = extract_markdown_links(text)
        self.assertEqual(result, expected_links)
        
    def test_extract_markdown_images(self):
        text = "This is a [link](https://example.com) and an ![image](https://example.com/image.png)."
        expected_images = [
            ("image", "https://example.com/image.png")
        ]
        result = extract_markdown_images(text)
        self.assertEqual(result, expected_images)
        
    def test_extract_markdown_links_no_links(self):
        text = "This is plain text with no links."
        expected_links = []
        result = extract_markdown_links(text)
        self.assertEqual(result, expected_links)
        
    def test_extract_markdown_links_escaped(self):
        text = "This is not a link: ![notalink](https://example.com) but this is a [link](https://example.com)."
        expected_links = [
            ("link", "https://example.com")
        ]
        result = extract_markdown_links(text)
        self.assertEqual(result, expected_links)
        
    def test_extract_markdown_links_multiple(self):
        text = "[first](https://first.com) and [second](https://second.com)"
        expected_links = [
            ("first", "https://first.com"),
            ("second", "https://second.com")
        ]
        result = extract_markdown_links(text)
        self.assertEqual(result, expected_links)
        
    def test_split_nodes_image(self):
        old_nodes = [TextNode("Here is an image ![alt text](https://example.com/image.png) in the text.", TextType.TEXT)]
        expected_nodes = [
            TextNode("Here is an image ", TextType.TEXT),
            TextNode("alt text", TextType.IMAGE, "https://example.com/image.png"),
            TextNode(" in the text.", TextType.TEXT)
        ]
        result = split_nodes_image(old_nodes)
        self.assertEqual(result, expected_nodes)
        
    def test_split_nodes_link(self):
        old_nodes = [TextNode("Here is a link [click here](https://example.com) in the text.", TextType.TEXT)]
        expected_nodes = [
            TextNode("Here is a link ", TextType.TEXT),
            TextNode("click here", TextType.LINK, "https://example.com"),
            TextNode(" in the text.", TextType.TEXT)
        ]
        result = split_nodes_link(old_nodes)
        self.assertEqual(result, expected_nodes)
        
    def test_text_to_textnodes(self):
        text = "This is **bold** text with a [link](https://example.com) and an ![image](https://example.com/image.png)."
        expected_nodes = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text with a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://example.com"),
            TextNode(" and an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://example.com/image.png"),
            TextNode(".", TextType.TEXT)
        ]
        result = text_to_textnodes(text)
        self.assertEqual(result, expected_nodes)
if __name__ == "__main__":
    unittest.main()