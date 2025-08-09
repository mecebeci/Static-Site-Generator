class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children if children is not None else []
        self.props = props if props is not None else {}

    def to_html(self):
        raise NotImplementedError("Subclasses must implement this method")
    
    def props_to_html(self):
        return " ".join(f'{key}="{value}"' for key, value in self.props.items())

    
    def __repr__(self):
        return f"Tag: {self.tag}\nValue: {self.value}\nChildren: {self.children}\nProps: {self.props_to_html()}"