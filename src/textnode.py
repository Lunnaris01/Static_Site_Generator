from enum import Enum
import re

class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"


class TextNode():
    def __init__(self,text,text_type,url=None):
        self.text = text
        self.text_type = TextType(text_type)
        self.url = url

    def __eq__(self,other):
        return (other.text == self.text and
            other.text_type == self.text_type and
            other.url == self.url)
    def __repr__(self):
        return f'TextNode({self.text}, {self.text_type.value}, {self.url})\n'


def split_nodes_delimiter(old_nodes,delimiters,text_types):
    sorted_inputs = sorted(zip(delimiters,text_types),key=lambda x: len(x[0]))[::-1]
    new_nodes = old_nodes.copy()
    for delim,t_type in sorted_inputs:
        new_nodes = _split_nodes_delimiter(new_nodes,delim,t_type)
    return new_nodes

def _split_nodes_delimiter(old_nodes,delimiter,text_type):
    ret_list = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            ret_list.append(node)
            continue
        textsplits= node.text.split(delimiter)
        for i, textsplit in enumerate(textsplits):
            if i%2 == 0 and textsplit != "":
                ret_list.append(TextNode(textsplit,node.text_type))
            elif i%2 == 1 and textsplit != "":
                ret_list.append(TextNode(textsplit,text_type))
    return ret_list


def extract_markdown_images(text):
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)",text)
    return matches

def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)",text)
    return matches

def split_nodes_images(old_nodes):
    ret_nodes = []
    for node in old_nodes:
        matches = extract_markdown_images(node.text)
        if not matches:
            ret_nodes.append(node)
            continue
        else:
            current_text = node.text
            for match in matches:
                splitterstring = f'![{match[0]}]({match[1]})'
                sections = current_text.split(splitterstring,1)
                if sections[0] != "":
                    ret_nodes.append(TextNode(sections[0],TextType.TEXT))
                ret_nodes.append(TextNode(match[0],TextType.IMAGE,match[1]))
                current_text = sections[1]
            if current_text != "":
                ret_nodes.append(TextNode(current_text,TextType.TEXT))
    return ret_nodes

def split_nodes_links(old_nodes):
    ret_nodes = []
    for node in old_nodes:
        matches = extract_markdown_links(node.text)
        if not matches:
            ret_nodes.append(node)
            continue
        else:
            current_text = node.text
            for match in matches:
                splitterstring = f'[{match[0]}]({match[1]})'
                sections = current_text.split(splitterstring,1)
                if sections[0] != "":
                    ret_nodes.append(TextNode(sections[0],TextType.TEXT))
                ret_nodes.append(TextNode(match[0],TextType.LINK,match[1]))
                current_text = sections[1]
            if current_text != "":
                ret_nodes.append(TextNode(current_text,TextType.TEXT))
    return ret_nodes

def text_to_textnodes(text):
    starting_node = [TextNode(text,TextType.TEXT)]
    updated_nodes = split_nodes_delimiter(starting_node,["*","**","`"],[TextType.ITALIC,TextType.BOLD,TextType.CODE])
    updated_nodes = split_nodes_images(updated_nodes)
    updated_nodes = split_nodes_links(updated_nodes)
    return updated_nodes