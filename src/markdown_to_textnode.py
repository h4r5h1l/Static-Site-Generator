from textnode import TextNode, TextType

def split_node_delimeter(old_nodes, delimeter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        if node.text.count(delimeter) % 2 != 0:
            raise ValueError(f"Unmatched delimeter {delimeter} in text: {node.text}")
        parts = node.text.split(delimeter)
        for i, part in enumerate(parts):
            if i % 2 == 0:
                new_nodes.append(TextNode(part, TextType.TEXT))
            else:
                new_nodes.append(TextNode(part, text_type))
    return new_nodes