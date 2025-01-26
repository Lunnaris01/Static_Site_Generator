from htmlnode import ParentNode, LeafNode,text_node_to_html_node
from textnode import text_to_textnodes

def markdown_to_blocks(markdown):
    ret_blocks = []
    currentline =""
    i = 0
    lines = markdown.split("\n")
    while i< len(lines):
        if lines[i] == "":
            i+=1
            continue
        elif lines[i].startswith("* ") or lines[i].startswith("- ") or lines[i].startswith(">"):
            combined_block = lines[i]
            while i+1<len(lines) and lines[i+1][0:2] == lines[i][0:2]:
                combined_block = f'{combined_block}\n{lines[i+1]}'
                i+=1
            ret_blocks.append(combined_block)
        elif lines[i].startswith("1."):
            counter = 1
            combined_block = lines[i]
            while i+1<len(lines) and any(lines[i+1].startswith(f"{j}. ") for j in range(1, 100)):
                counter +=1
                i+=1
                combined_block = f'{combined_block}\n{lines[i+1]}'
            ret_blocks.append(combined_block)
        elif lines[i].startswith("```"):
            if len(lines[i].split("```"))>2:  # single-line code block
                ret_blocks.append(lines[i])
                i+=1
                continue
            combined_block = lines[i]
            i += 1
            # Keep adding lines until we either find closing ``` or reach end of document
            while i < len(lines):
                combined_block = f'{combined_block}\n{lines[i]}'
                if lines[i].startswith("```"):
                    break
                i += 1
            ret_blocks.append(combined_block)
        else:
            combined_block = lines[i].strip()
            while i+1 < len(lines) and lines[i+1] and not (
                lines[i+1].startswith(("* ", "- ", ">", "1.", "```", "#"))
            ):
                i += 1
                combined_block = f'{combined_block}\n{lines[i].strip()}'
            ret_blocks.append(combined_block)
        i+=1
    return ret_blocks


def block_to_block_type(block):
    lines = block.split("\n")

    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return "header"
    elif len(lines) > 1 and lines[0].startswith("```") and lines[-1].startswith("```"):
        return "code" 
    elif block.startswith(">"):
        for line in lines:
            if not line.startswith(">"):
                return "paragraph"
        return "quote"
    elif block.startswith("* "):
        for line in lines:
            if not line.startswith("* "):
                return "paragraph"
        return "unordered_list"
    elif block.startswith("- "):
        for line in lines:
            if not line.startswith("- "):
                return "paragraph"
        return "unordered_list"
    elif any(line.strip().startswith(f"{i}. ") for i in range(1, 100) for line in lines):
        # Check if the majority of non-empty lines start with a number
        non_empty_lines = [l for l in lines if l.strip()]
        numbered_lines = [l for l in non_empty_lines if any(
            l.strip().startswith(f"{i}. ") for i in range(1, 100)
        )]
        if len(numbered_lines) / len(non_empty_lines) >= 0.5:
            return "ordered_list"
    return "paragraph" 


""" def block_to_block_type(blockstring):
    if blockstring[0] == '#':
        return "header"
    if blockstring[0:3] == '```':
        return "code" 
    if blockstring.startswith(">"):
        for line in lines:
            if not line.startswith(">"):
                return "paragraph"
        return "quote"
    if blockstring.startswith("* "):
        for line in lines:
            if not line.startswith("* "):
                return block_type_paragraph
        return "unordered_list"
    if blockstring.startswith("- "):
        for line in lines:
            if not line.startswith("- "):
                return block_type_paragraph
        return "unordered_list"
    if blockstring.startswith("1. "):
        i = 1
        for line in lines:
            if not line.startswith(f"{i}. "):
                return block_type_paragraph
            i += 1
        return "ordered_list"

    else:
        return "paragraph"
 """    

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    all_blocks = []
    for block in blocks:
        blocktype = block_to_block_type(block)

        if blocktype == "paragraph":
            node = ParentNode("p",None)
            children = text_to_children(block.strip())
            node.children = children
            all_blocks.append(node)
        elif blocktype == "header":
            i = 0
            while i<len(block):
                if block[i] == '#':
                    i +=1
                    continue
                break
            headertag = f'h{i}'
            children = text_to_children(block[i:].strip())
            node = ParentNode(headertag,children)
            all_blocks.append(node)
        elif blocktype == "code":
            content = block[3:-3].strip()
            prenode = ParentNode("pre",None)
            codenode = LeafNode("code",content)
            prenode.children = [codenode]
            all_blocks.append(prenode)
        elif blocktype == "quote":
            node = ParentNode("blockquote", None)
            # Split into lines, remove '>' from each line, and rejoin
            lines = block.split('\n')
            cleaned_lines = []
            for line in lines:
                line = line.strip()
                if line.startswith('>'):
                    line = line[1:].strip()
                cleaned_lines.append(line)
            cleaned_block = '\n'.join(cleaned_lines)
            children = text_to_children(cleaned_block)
            node.children = children
            all_blocks.append(node)        
        elif blocktype == "unordered_list":
            list_node = ParentNode("ul",None)
            # Need to split into items and handle each one
            # Each line starts with "- " or "* "
            items = block.split("\n")
            list_items = []
            for item in items:
                # Remove the "- " or "* " and create li node
                item_text = item[2:].strip()  # Remove marker and whitespace
                li_node = ParentNode("li",None)
                li_node.children = text_to_children(item_text)
                list_items.append(li_node)
            list_node.children = list_items
            all_blocks.append(list_node)
        elif blocktype == "ordered_list":
            list_node = ParentNode("ol", None)
            items = block.split("\n")
            list_items = []
            for item in items:
                # Skip empty lines
                if not item.strip():
                    continue
                # Find the position after the number and dot
                item_text = item.strip()
                for i in range(len(item_text)):
                    if item_text[i:].startswith(". "):
                        item_text = item_text[i+2:].strip()
                        break
                # Create li node with the extracted text
                li_node = ParentNode("li", None)
                li_node.children = text_to_children(item_text)
                list_items.append(li_node)
            list_node.children = list_items
            all_blocks.append(list_node)
    divnode = ParentNode("div",all_blocks)
    return divnode



    
def text_to_children(text):
    # First get the text nodes
    text_nodes = text_to_textnodes(text)
    htmlnodes = []
    for node in text_nodes:
        htmlnodes.append(text_node_to_html_node(node))
    return htmlnodes
