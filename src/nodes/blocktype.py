import unittest
import re
from enum import Enum


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered list"
    ORDERED_LIST = "ordered list"


class MarkdownParser:
    def block_to_block_type(self, block_text):
        if bool(re.match(r'^(#{1,6})\s.+$', block_text)):
            return BlockType.HEADING
        
        elif block_text.startswith("```") and block_text.endswith("```"):
            return BlockType.CODE
        
        elif block_text.startswith(">"):
            return BlockType.QUOTE
        
        elif block_text.startswith("- "):
            return BlockType.UNORDERED_LIST
        
        elif self.is_ordered_list(block_text):
            return BlockType.ORDERED_LIST
        
        else:
            return BlockType.PARAGRAPH

    def is_ordered_list(self, block_text):
        lines = block_text.strip().split("\n")
        for i, line in enumerate(lines, start=1):
            if not re.match(rf'^{i}\. .+$', line):
                return False
        return True

