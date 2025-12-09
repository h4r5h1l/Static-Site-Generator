from htmlnode import HtmlNode

class LeafNode(HtmlNode):
    def __init__(self, tag: str=None, value: str=None, props: dict[str, str]=None):
        super().__init__(tag=tag, value=value, props=props)
        
    def to_html(self) -> str:
        if self.value is None:
            raise(ValueError("LeafNode must have a value."))
        if self.tag is None:
            return self.value
        if not self.props:
            return f"<{self.tag}>{self.value}</{self.tag}>"
        return f"<{self.tag} {self.props_to_html()}>".strip() + self.value + f"</{self.tag}>"
    
    def __repr__(self):
        return f"LeafNode(tag={self.tag}, value={self.value}, props={self.props})"