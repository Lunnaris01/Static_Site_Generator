from textnode import TextNode, TextType


class HTMLNode():
    def __init__(self,tag=None,value=None,children=None,props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("function not yet implemented")

    def props_to_html(self):
        props_html_str = ""
        if self.props:
            for key,value in self.props.items():
                props_html_str = props_html_str + f' {key}=\"{value}\"'
        return props_html_str

    def __repr__(self):
        return f'- HTMLNode -\nTag:{self.tag}\nValue:{self.value}\nChildren:{self.children}\nProps:{self.props}'


class LeafNode(HTMLNode):
    def __init__(self,tag,value,props=None):
        super().__init__(tag,value,None,props)

    def to_html(self):
        if self.value==None:
            raise ValueError("Leafnode has no value")
        if not self.tag:
            return self.value
        return f'<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>'

class ParentNode(HTMLNode):
    def __init__(self,tag,children,props=None):
        super().__init__(tag,None,children,props)
        if not children:
            self.children = []

    def to_html(self):
        if not self.tag:
            raise ValueError("ParentNode is missing tag")
        if not all(isinstance(child, HTMLNode) for child in self.children):
            raise ValueError("All children must be instances of HTMLNode (e.g., LeafNode or ParentNode)")
        childhtml = " ".join(map(lambda x:x.to_html(),self.children))
        
        return f'<{self.tag}{self.props_to_html()}>{childhtml}</{self.tag}>'

def text_node_to_html_node(text_node):
    match(text_node.text_type):
        case TextType.TEXT:
            return LeafNode(tag=None,value = text_node.text)
        case TextType.BOLD:
            return LeafNode(tag="b",value = text_node.text)
        case TextType.ITALIC:
            return LeafNode(tag="i",value = text_node.text)
        case TextType.CODE:
            return LeafNode(tag="code",value = text_node.text)
        case TextType.LINK:
            return LeafNode(tag="a",value = text_node.text, props={"href":text_node.url})
        case TextType.IMAGE:
            return LeafNode(tag="img",value = "", props = {"src":text_node.url,"alt":text_node.text})
        case _:
            raise Exception("Unknown Text Type")
