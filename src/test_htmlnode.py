import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode, text_node_to_html_node
from textnode import TextNode, TextType


class TestHTMLNode(unittest.TestCase):
    def test_uninitialized_1(self):
        node = HTMLNode(tag="a", value="Link")
        self.assertEqual(node.children, None)
        self.assertEqual(node.props,None)

    def test_init(self):
        node = HTMLNode(tag="a", value="Link", props={"href":"www.boot.dev"})
        self.assertEqual(node.tag, "a")
        self.assertEqual(node.value, "Link")
        self.assertEqual(node.props,{"href":"www.boot.dev"})

    def test_repr(self):
        childnode = HTMLNode(tag="p")
        node = HTMLNode(tag="h1", value = "Test", children =[childnode])
        expected = "- HTMLNode -\nTag:h1\nValue:Test\nChildren:[- HTMLNode -\nTag:p\nValue:None\nChildren:None\nProps:None]\nProps:None"
        actual = str(node)
        self.assertEqual(expected,actual)

class TestLeafNode(unittest.TestCase):
    def test_init_1(self):
        node = LeafNode("a","Link",{"href":"www.boot.dev"})
        self.assertEqual(node.children, None)
        self.assertEqual(node.tag, "a")
        self.assertEqual(node.value, "Link")
        self.assertEqual(node.props,{"href":"www.boot.dev"})

    def test_link_to_html(self):
        node = LeafNode("a","Link",{"href":"www.boot.dev"})
        self.assertEqual(node.to_html(),"<a href=\"www.boot.dev\">Link</a>")

    def test_no_tag_to_html(self):
        node = LeafNode(tag=None,value="Untagged Leafnode!")
        self.assertEqual(node.to_html(),"Untagged Leafnode!")

    def test_no_value_error(self):
        node = LeafNode(tag=None,value=None)
        with self.assertRaisesRegex(ValueError,"Leafnode has no value"):
            node.to_html()

class TestParentNode(unittest.TestCase):
    def test_parent_leaf(self):
        childnode = LeafNode(tag = "p",value="This is a Leafnode")
        parentNode = ParentNode(tag = "h1",children =[childnode],props = {"color":"red"})
        self.assertEqual(parentNode.to_html(),"<h1 color=\"red\"><p>This is a Leafnode</p></h1>")

    def test_parent_parent_leaf(self):
        childnode = LeafNode(tag = "p",value="This is a Leafnode")
        parentNode_1 = ParentNode(tag = "a", children =[childnode])
        parentNode_2 = ParentNode(tag = "h1",children =[parentNode_1],props = {"color":"red"})
        self.assertEqual(parentNode_2.to_html(),"<h1 color=\"red\"><a><p>This is a Leafnode</p></a></h1>")
        
    def test_no_children(self):
        parentNode = ParentNode("a",None)
        with self.assertRaisesRegex(ValueError,"ParentNode has no Children \(should be LeafNode!\)"):
            parentNode.to_html()

    def test_no_children_emptylist(self):
        parentNode = ParentNode("a",[])
        with self.assertRaisesRegex(ValueError,"ParentNode has no Children \(should be LeafNode!\)"):
            parentNode.to_html()

    def test_children_no_Node(self):
        parentNode = ParentNode("a",["I am a Leafnode and not a string I swear!!!"])
        with self.assertRaises(ValueError) as context:
            parentNode.to_html()
            self.assertTrue("must be instances of HTMLNode" in context)
    

    def test_no_children_2(self):
        parentNode = ParentNode("a",None)
        parentNode_2 = ParentNode("b",[parentNode])
        with self.assertRaisesRegex(ValueError,"ParentNode has no Children \(should be LeafNode!\)"):
            parentNode_2.to_html()

    def test_no_tag(self):
        parentNode = ParentNode(None,[LeafNode("p","value")])
        with self.assertRaisesRegex(ValueError,"ParentNode is missing tag"):
            parentNode.to_html()

class TestTextNodeToLeadNode(unittest.TestCase):
    def test_syntax(self):

        test_cases = [(TextType.TEXT,None),
                      (TextType.BOLD,"b"),
                      (TextType.ITALIC,"i"),
                      (TextType.CODE,"code"),
                      (TextType.LINK,"a"),
                      (TextType.IMAGE,"img")]

        for text_type, expected_tag in test_cases:
            node = TextNode("Sample Text", text_type)
            converted_node = text_node_to_html_node(node)
            self.assertEqual(converted_node.tag, expected_tag)



if __name__ == "__main__":
    unittest.main()
