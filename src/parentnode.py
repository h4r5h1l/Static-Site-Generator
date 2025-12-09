from htmlnode import HtmlNode

class ParentNode(HtmlNode):
    def __init__(self, tag: str=None, children: list[HtmlNode]=None, props: dict[str, str]=None):
        super().__init__(tag=tag, children=children, props=props)
        
    def to_html(self) -> str:
        if self.tag is None:
            raise(ValueError("ParentNode must have a tag."))
        if self.children is None or len(self.children) == 0:
            raise(ValueError("ParentNode must have children."))
        # recursive call to get children's HTML
        children_html = "".join(child.to_html() for child in self.children)
        if not self.props:
            return f"<{self.tag}>{children_html}</{self.tag}>"
        return f"<{self.tag} {self.props_to_html()}>".strip() + children_html + f"</{self.tag}>"
    
    def __repr__(self):
        return f"ParentNode(tag={self.tag}, children={self.children}, props={self.props})"