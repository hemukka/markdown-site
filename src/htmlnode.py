
class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props:dict=None ):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("to_html method not implemented")
    
    def props_to_html(self):
        """ Return string that represents the HTML attributes of the node. """
        html = ""
        if not self.props:
            return html
        for prop in self.props:
            html += f' {prop}="{self.props[prop]}"'
        return html

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, children: {self.children}, {self.props})"
    

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props:dict=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        """ Return LeafNode as HTML formatted string. """
        if self.value is None:
            raise ValueError("leaf node's value missing")
        if not self.tag:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
        
    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"
    

class ParentNode(HTMLNode):
    def __init__(self, tag, children: list, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        """ Return ParentNode as HTML formatted string.
         Recursively call children to get their HTML formatted strings.
         """
        if not self.tag:
            raise ValueError("parent node's tag missing")
        
        if not self.children:
            raise ValueError("parent node's children missing")

        return f"<{self.tag}>{"".join(map(lambda child: child.to_html(), self.children))}</{self.tag}>"
    
    def __repr__(self):
        return f"ParentNode({self.tag}, children: {self.children}, {self.props})"