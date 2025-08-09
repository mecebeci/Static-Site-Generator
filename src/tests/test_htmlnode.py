import unittest

from nodes.htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_empty_props(self):
        node = HTMLNode()
        print(node.props_to_html())

    def test_one_value_props(self):
        dict_prop = {"href": "https://wwww.google.com"}
        node = HTMLNode(dict_prop)
        print(node.props_to_html())

    def test_one_value_props(self):
        dict_prop = {"href": "https://wwww.google.com", "target": "_blank"}
        node = HTMLNode(dict_prop)
        print(node.props_to_html())