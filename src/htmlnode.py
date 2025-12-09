class HtmlNode:
    def __init__(self, tag: str=None, value: str=None, children: list["HtmlNode"]=None, props: dict[str, str]=None):
        self.tag = tag
        self.value = value
        self.children = children if children is not None else []
        self.props = props if props is not None else {}
        
    def to_html(self) -> str:
        raise NotImplementedError("to_html method is not implemented yet.")
        # if self.tag is None:
        #     return self.value or ""
        
        # props_str = " ".join(f'{key}="{value}"' for key, value in self.props.items())
        # opening_tag = f"<{self.tag} {props_str}>".strip()
        # closing_tag = f"</{self.tag}>"
        
        # children_html = "".join(child.to_html() for child in self.children)
        
        # return f"{opening_tag}{self.value or ''}{children_html}{closing_tag}"
        
    def props_to_html(self):
        return " ".join(f'{key}="{value}"' for key, value in self.props.items())
    
    def __repr__(self):
        return f"HtmlNode(tag={self.tag}, value={self.value}, children={self.children}, props={self.props})"