import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):

    a_attributes = {
    "href": "https://www.google.com",
    "target": "_blank",
    }

    def test_props_to_html(self):
        node = HTMLNode("a", "link to somewhere", None, self.a_attributes)
        self.assertEqual(
            ' href="https://www.google.com" target="_blank"',
            node.props_to_html()
        )

    def test_props_to_html_none(self):
        node = HTMLNode("a", "link to somewhere")
        self.assertEqual('', node.props_to_html())

    def test_repr(self):
        node = HTMLNode("a", "link to somewhere", None, self.a_attributes)
        self.assertEqual(
            f"HTMLNode(a, link to somewhere, children: None, {self.a_attributes})",
            repr(node)
        )

class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")

    def test_leaf_to_html_no_value(self):
        node = LeafNode(None, None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_b(self):
        node = LeafNode("b", "Hello, world!")
        self.assertEqual(node.to_html(), "<b>Hello, world!</b>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')

    def test_leaf_repr(self):
        node = LeafNode("a", "link to somewhere", {"href": "https://www.google.com"})
        self.assertEqual(
            "LeafNode(a, link to somewhere, {'href': 'https://www.google.com'})",
            repr(node)
        )

class TestParentNode(unittest.TestCase):
    def test_parent_to_html_no_tag(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode(None, [child_node])
        with self.assertRaises(ValueError):
            parent_node.to_html()

    def test_parent_to_html_no_children(self):
        parent_node = ParentNode("div", None)
        with self.assertRaises(ValueError):
            parent_node.to_html()

    def test_parent_to_html_no_children_value(self):
        child_node = LeafNode("span", None)
        parent_node = ParentNode(None, [child_node])
        with self.assertRaises(ValueError):
            parent_node.to_html()

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_many_children(self):
        parent_node = ParentNode("p", [
            LeafNode("b", "Bold text"),
            LeafNode(None, "Normal text"),
            LeafNode("i", "italic text"),
            LeafNode(None, "Normal text"),
        ])
        self.assertEqual(parent_node.to_html(),
                         "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

if __name__ == "__main__":
    unittest.main()