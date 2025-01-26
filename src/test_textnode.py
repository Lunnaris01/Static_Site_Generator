import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_not_eq(self):
        node = TextNode("This is a text node", TextType.BOLD,"")
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_enum(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", "bold")
        print('\nExpected: True')
        print(f'\nActual: {node == node2}')
        self.assertEqual(node, node2)



    def test_repr(self):
        node = TextNode("We are testing the printing","bold","https://www.boot.dev")
        expected = f'TextNode({"We are testing the printing"}, {"bold"}, {"https://www.boot.dev"})\n'
        print(f'\nExpected: {expected}')
        actual = str(node)
        print(f'\nActual:  {actual}')
        self.assertEqual(expected, actual)


if __name__ == "__main__":
    unittest.main()
