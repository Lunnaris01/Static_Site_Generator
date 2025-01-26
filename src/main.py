import textnode, htmlnode

def main():
    text_node = textnode.TextNode("Sample node","bold","https://www.boot.dev")
    #print(str(text_node))
    childnode = htmlnode.LeafNode(tag = "p",value="This is a Leafnode")
    htmlNode = htmlnode.HTMLNode(tag = "a", value = "Click Here",children = [childnode],props = {"href":"https://www.boot.dev"})
    #print(str(htmlNode))
    #print(htmlNode.props_to_html())

    parentNode = htmlnode.ParentNode(tag = "h1",children =[childnode],props = {"color":"red"})
    print(parentNode)
    print(parentNode.to_html())

    updated_nodes = [textnode.TextNode("This is a ** note ** with bold and * italic * and `code` in it!",textnode.TextType("text"))]
    
    updated_nodes = textnode.split_nodes_delimiter(updated_nodes,["*","**","`"],[textnode.TextType("italic"),textnode.TextType("bold"),textnode.TextType("code")])
    print(updated_nodes)
    node_list = textnode.text_to_textnodes("This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)")
    print(node_list)




if __name__ == "__main__":
    main()
