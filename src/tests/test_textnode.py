import unittest

from nodes.textnode import *
from functions import *


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_not_eq(self):
        node = TextNode("This is not a text node", TextType.TEXT)
        node2 = TextNode("This is a text node", TextType.TEXT)
        self.assertNotEqual(node, node2)

    def test_property(self):
        node = TextNode("Italic", TextType.ITALIC)
        node2 = TextNode("Not Italic", TextType.ITALIC)
        self.assertEqual(node.text_type, node2.text_type)

    def test_url(self):
        node = TextNode("Ha ha", TextType.CODE)
        node2 = TextNode("Ho ho", TextType.CODE, None)
        self.assertEqual(node.url, node2.url)

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_code(self):
        node = TextNode("This is a code node", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is a code node")

if __name__ == "__main__":
    unittest.main()