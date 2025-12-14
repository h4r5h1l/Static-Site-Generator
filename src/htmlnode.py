class HtmlNode:
    def __init__(self, tag: str=None, value: str=None, children: list["HtmlNode"]=None, props: dict[str, str]=None):
        self.tag = tag
        self.value = value
        self.children = children if children is not None else []
        self.props = props if props is not None else {}
        
    def to_html(self) -> str:
        raise NotImplementedError("to_html method is not implemented yet.")
        # Child classes should override this method to render themselves as HTML.
    def props_to_html(self):
        return " ".join(f'{key}="{value}"' for key, value in self.props.items())
    
    @staticmethod
    def text_node_to_html_node(text_node):
        # Convert a TextNode to its HTML string representation
        from src.textnode import TextNode
        node = TextNode.text_node_to_html_node(text_node)
        if isinstance(node, HtmlNode):
            return node.to_html()
        return str(node)

    def __eq__(self, other):
        if not isinstance(other, HtmlNode):
            return False
        return (
            self.tag == other.tag and
            self.value == other.value and
            self.children == other.children and
            self.props == other.props
        )

    def __repr__(self):
        return f"HtmlNode(tag={self.tag}, value={self.value}, children={self.children}, props={self.props})"

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
    
class LeafNode(HtmlNode):
    def __init__(self, tag: str=None, value: str=None, props: dict[str, str]=None):
        super().__init__(tag=tag, value=value, props=props)
        
    def to_html(self) -> str:
        # If no tag, it must have a value and return plain text
        if self.tag is None:
            if self.value is None:
                raise(ValueError("LeafNode must have a value."))
            return self.value

        # If tag is present but value is None, render as self-closing only for void elements
        if self.value is None:
            void_tags = {"img", "br", "hr", "input", "meta", "link"}
            if self.tag in void_tags:
                if self.props:
                    return f"<{self.tag} {self.props_to_html()}/>"
                return f"<{self.tag}/>"
            raise(ValueError("LeafNode must have a value."))

        # Normal tag with value
        if not self.props:
            return f"<{self.tag}>{self.value}</{self.tag}>"
        return f"<{self.tag} {self.props_to_html()}>".strip() + self.value + f"</{self.tag}>"
    
    def __repr__(self):
        return f"LeafNode(tag={self.tag}, value={self.value}, props={self.props})"