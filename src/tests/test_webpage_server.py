import unittest
import tempfile, os, shutil
from src.webpage_server import extract_title, generate_page, generate_pages_recursively

class TestWebpageServer(unittest.TestCase):
    def test_extract_title(self):
        markdown = "# Sample Title"
        title = extract_title(markdown)
        self.assertEqual(title, "Sample Title")
        
    def test_no_title(self):
        markdown = "This is a paragraph without a title."
        with self.assertRaises(ValueError):
            extract_title(markdown)
            
    def test_generate_page(self):
        from_path = "sample.md"
        template_path = "template.html"
        with open(from_path, "w") as f:
            f.write("# Sample Title\n\nThis is a paragraph.")
        # create a simple template with Title and Content placeholders
        with open(template_path, "w") as f:
            f.write("<html><head><title>{{ Title }}</title></head><body>{{ Content }}</body></html>")
        html = generate_page(from_path, template_path, dest_path="output.html")
        self.assertIn('<h1>Sample Title</h1>', html)
        self.assertIn('<p>This is a paragraph.</p>', html)
        # cleanup files created by the test
        import os
        for path in (from_path, template_path, "output.html"):
            try:
                os.remove(path)
            except OSError:
                pass

    def test_generate_pages_recursively(self):
        tmpdir = tempfile.mkdtemp()
        try:
            # create nested content structure
            content_dir = os.path.join(tmpdir, "content")
            os.makedirs(os.path.join(content_dir, "blog", "alice"))
            # top-level index
            with open(os.path.join(content_dir, "index.md"), "w") as f:
                f.write("# Home\n\nWelcome home.")
            # nested blog post
            with open(os.path.join(content_dir, "blog", "alice", "index.md"), "w") as f:
                f.write("# Alice\n\nAlice's post.")

            template_path = os.path.join(tmpdir, "template.html")
            with open(template_path, "w") as f:
                f.write("<html><head><title>{{ Title }}</title></head><body>{{ Content }}</body></html>")

            dest_dir = os.path.join(tmpdir, "public")
            # generate recursively and capture generated paths
            generated = generate_pages_recursively(content_dir, template_path, dest_dir)

            # assert files created and returned
            top_out = os.path.join(dest_dir, "index.html")
            nested_out = os.path.join(dest_dir, "blog", "alice", "index.html")
            self.assertTrue(os.path.isfile(top_out))
            self.assertTrue(os.path.isfile(nested_out))
            self.assertIn(top_out, generated)
            self.assertIn(nested_out, generated)
            # check contents
            with open(top_out, "r") as f:
                top_html = f.read()
            with open(nested_out, "r") as f:
                nested_html = f.read()

            self.assertIn("<h1>Home</h1>", top_html)
            self.assertIn("<p>Welcome home.</p>", top_html)
            self.assertIn("<h1>Alice</h1>", nested_html)
            self.assertIn("<p>Alice's post.</p>", nested_html)
        finally:
            shutil.rmtree(tmpdir)

    def test_generate_pages_recursively_returns_map(self):
        import tempfile, os, shutil
        tmpdir = tempfile.mkdtemp()
        try:
            # create nested content structure
            content_dir = os.path.join(tmpdir, "content")
            os.makedirs(os.path.join(content_dir, "blog", "bob"))
            # top-level index
            with open(os.path.join(content_dir, "index.md"), "w") as f:
                f.write("# Home\n\nWelcome home.")
            # nested blog post
            src_nested = os.path.join(content_dir, "blog", "bob", "index.md")
            with open(src_nested, "w") as f:
                f.write("# Bob\n\nBob's post.")

            template_path = os.path.join(tmpdir, "template.html")
            with open(template_path, "w") as f:
                f.write("<html><head><title>{{ Title }}</title></head><body>{{ Content }}</body></html>")

            dest_dir = os.path.join(tmpdir, "public")
            # generate recursively and get mapping
            mapping = generate_pages_recursively(content_dir, template_path, dest_dir, return_map=True)

            # expected dest
            expected_nested = os.path.join(dest_dir, "blog", "bob", "index.html")
            self.assertIn(src_nested, mapping)
            self.assertEqual(mapping[src_nested], expected_nested)

        finally:
            shutil.rmtree(tmpdir)

        

if __name__ == "__main__":
    unittest.main()