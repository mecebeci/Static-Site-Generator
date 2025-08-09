import unittest

from functions import extract_markdown_images, extract_markdown_links

class TestExtractFunctions(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)")
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links("This is text with [regexr.com](https://regexr.com)")
        self.assertListEqual([("regexr.com", "https://regexr.com")], matches)

        