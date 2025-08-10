import unittest
from nodes.blocktype import *

class TestBlockToBlockTypeFunction(unittest.TestCase):
    def setUp(self):
        self.parser = MarkdownParser()
    
    def test_heading(self):
        block_text = "### Header 3"
        result = self.parser.block_to_block_type(block_text)
        self.assertEqual(result, BlockType.HEADING)

    def test_code(self):
        block_text = "```\nprint('Hello')\n```"
        result = self.parser.block_to_block_type(block_text)
        self.assertEqual(result, BlockType.CODE)

    def test_quote(self):
        block_text = "> This is a quote"
        result = self.parser.block_to_block_type(block_text)
        self.assertEqual(result, BlockType.QUOTE)

    def test_unordered_list(self):
        block_text = "- Item 1\n- Item 2"
        result = self.parser.block_to_block_type(block_text)
        self.assertEqual(result, BlockType.UNORDERED_LIST)

    def test_ordered_list(self):
        block_text = "1. First\n2. Second\n3. Third"
        result = self.parser.block_to_block_type(block_text)
        self.assertEqual(result, BlockType.ORDERED_LIST)

    def test_paragraph(self):
        block_text = "This is a normal paragraph."
        result = self.parser.block_to_block_type(block_text)
        self.assertEqual(result, BlockType.PARAGRAPH)
