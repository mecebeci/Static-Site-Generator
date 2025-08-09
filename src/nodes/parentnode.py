from nodes.htmlnode import HTMLNode

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, value=None, children=children, props=props)

    def to_html(self):
        if not self.tag:
            raise ValueError("Node need to has a value")
        
        if not self.children:
            raise ValueError("Node need to has children")
        
        result = f"<{self.tag}>"
        for child in self.children:
            result += child.to_html()
        result += f"</{self.tag}>"

        return result