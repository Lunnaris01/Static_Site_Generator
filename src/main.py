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


if __name__ == "__main__":
    main()
