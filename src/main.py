import textnode, htmlnode
from markdown_blocks import markdown_to_html_node
from publish_static import prepare_public,copy_content,generate_page,generate_pages_recursive

def main():
    # text_node = textnode.TextNode("Sample node","bold","https://www.boot.dev")
    # #print(str(text_node))
    # childnode = htmlnode.LeafNode(tag = "p",value="This is a Leafnode")
    # htmlNode = htmlnode.HTMLNode(tag = "a", value = "Click Here",children = [childnode],props = {"href":"https://www.boot.dev"})
    # #print(str(htmlNode))
    # #print(htmlNode.props_to_html())

    # parentNode = htmlnode.ParentNode(tag = "h1",children =[childnode],props = {"color":"red"})
    # #print(parentNode)
    # #print(parentNode.to_html())

    # updated_nodes = [textnode.TextNode("This is a ** note ** with bold and * italic * and `code` in it!",textnode.TextType("text"))]
    
    # updated_nodes = textnode.split_nodes_delimiter(updated_nodes,["*","**","`"],[textnode.TextType("italic"),textnode.TextType("bold"),textnode.TextType("code")])
    # #print(updated_nodes)
    # node_list = textnode.text_to_textnodes("This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)")
    # #print(node_list)

    # doc = "# My Title\n\nThis is a paragraph with some *italic* and **bold** text.\n\n## Subtitle\n\nHere's a list:\n* First item\n* Second item\n* Third item\n\nAnd an ordered list:\n1. First\n2. Second\n3. Third\n\n> This is a blockquote\n> with multiple lines\n\nHere's some code:\n```\ndef hello():\n    print(\"Hello, world!\")\n```"
    # node = markdown_to_html_node(doc)
    # #print(node.to_html())
    prepare_public("public/","static/")
    copy_content("public/","static/")
    generate_pages_recursive("content/","template.html","public/")



if __name__ == "__main__":
    main()
