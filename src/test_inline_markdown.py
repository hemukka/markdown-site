import unittest

from textnode import TextType, TextNode
from inline_markdown import (
    text_to_textnodes,
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
    extract_markdown_images,
    extract_markdown_links
)

class TestInlineMarkdown(unittest.TestCase):
    def test_delimiter_text(self):
        # just text should remain as is
        nodes = [TextNode("This is text", TextType.TEXT)]
        self.assertEqual(split_nodes_delimiter(nodes, "'", TextType.CODE), nodes)
        
    def test_delimiter_non_text(self):
        # bold, italic, code, link, image all should remain as is
        nodes = [TextNode("This is bolded text", TextType.BOLD),
                 TextNode("This is italic text", TextType.ITALIC),
                 TextNode("This is code text", TextType.CODE),
                 TextNode("This is link text", TextType.LINK),
                 TextNode("This is image text", TextType.IMAGE)]
        self.assertEqual(split_nodes_delimiter(nodes, "'", TextType.CODE), nodes)
        
    def test_delimiter_bold_middle(self):
        # text with bold should be split into 3 nodes
        nodes = [TextNode("This is text with a **bolded phrase** in the middle", TextType.TEXT)]
        new_nodes = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("bolded phrase", TextType.BOLD),
            TextNode(" in the middle", TextType.TEXT),
        ]
        self.assertEqual(split_nodes_delimiter(nodes, "**", TextType.BOLD), new_nodes)

    def test_delimiter_bold_start(self):
        # text with bold at the start of the text should be split into 2 nodes
        nodes = [TextNode("**This is text with a bolded phrase** at the start", TextType.TEXT)]
        new_nodes = [
            TextNode("This is text with a bolded phrase", TextType.BOLD),
            TextNode(" at the start", TextType.TEXT),
        ]
        self.assertEqual(split_nodes_delimiter(nodes, "**", TextType.BOLD), new_nodes)

    def test_delimiter_bold_end(self):
        # text with bold at the end of the text should be split into 2 nodes
        nodes = [TextNode("This is text with a bolded phrase at **the end**", TextType.TEXT)]
        new_nodes = [
            TextNode("This is text with a bolded phrase at ", TextType.TEXT),
            TextNode("the end", TextType.BOLD),
        ]
        self.assertEqual(split_nodes_delimiter(nodes, "**", TextType.BOLD), new_nodes)

    def test_delimiter_bold_double(self):
        # text with 2 bold sections should be split into 5 nodes
        nodes = [TextNode("This is **text** with **bolded phrases** in the middle", TextType.TEXT)]
        new_nodes = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with ", TextType.TEXT),
            TextNode("bolded phrases", TextType.BOLD),
            TextNode(" in the middle", TextType.TEXT),
        ]
        self.assertEqual(split_nodes_delimiter(nodes, "**", TextType.BOLD), new_nodes)

    def test_delimiter_italic(self):
        # text with italic should be split into 3 nodes
        nodes = [TextNode("This is text with a _italic phrase_ in the middle", TextType.TEXT)]
        new_nodes = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("italic phrase", TextType.ITALIC),
            TextNode(" in the middle", TextType.TEXT),
        ]
        self.assertEqual(split_nodes_delimiter(nodes, "_", TextType.ITALIC), new_nodes)

    def test_delimiter_code(self):
        # text with code block should be split into 3 nodes
        nodes = [TextNode("This is text with a `code block` in the middle", TextType.TEXT)]
        new_nodes = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" in the middle", TextType.TEXT),
        ]
        self.assertEqual(split_nodes_delimiter(nodes, "`", TextType.CODE), new_nodes)

    def test_delimiter_multiple(self):
        # text with bold, italic and code block should be split correctly when called for each type
        nodes = [TextNode("This is text with **bold text**, _italic text_ and `code block` in the middle", TextType.TEXT)]
        new_nodes = [
            TextNode("This is text with ", TextType.TEXT),
            TextNode("bold text", TextType.BOLD),
            TextNode(", ", TextType.TEXT),
            TextNode("italic text", TextType.ITALIC),
            TextNode(" and ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" in the middle", TextType.TEXT)
        ]
        self.assertEqual(
            split_nodes_delimiter(
                split_nodes_delimiter(
                    split_nodes_delimiter(nodes, "`", TextType.CODE),
                    "_", TextType.ITALIC),
                "**", TextType.BOLD),
            new_nodes
        )

    def test_delimiter_missing_delimiter(self):
        # text with missing closing delimiter should raise exception
        nodes = [TextNode("This is text with a `code block but without closing delimiter", TextType.TEXT)]
        with self.assertRaises(Exception):
            split_nodes_delimiter(nodes)

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_images_start(self):
        node = TextNode(
            "![image](https://i.imgur.com/zjjcJKZ.png) at the start and another ![second image](https://i.imgur.com/3elNhQu.png) in the middle",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" at the start and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
                TextNode(" in the middle", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_images_zero(self):
        node = TextNode(
            "This is text without any images.",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text without any images.", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](https://i.imgur.com) and another [second link](https://i.imgur.com/)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://i.imgur.com"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second link", TextType.LINK, "https://i.imgur.com/"
                ),
            ],
            new_nodes,
        )

    def test_split_links_zero(self):
        node = TextNode(
            "This is text without any links.",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text without any links.", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_text(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            nodes
        )

    def test_text_2(self):
        text = "![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg)`code block`[link](https://boot.dev)_italic_**text**"
        nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode("code block", TextType.CODE),
                TextNode("link", TextType.LINK, "https://boot.dev"),
                TextNode("italic", TextType.ITALIC),
                TextNode("text", TextType.BOLD),
            ],
            nodes
        )


class TestExtractMarkdown(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_images_multiple(self):
        matches = extract_markdown_images(
            "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        )
        self.assertListEqual([("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with an [link](https://i.imgur.com)"
        )
        self.assertListEqual([("link", "https://i.imgur.com")], matches)

    def test_extract_markdown_links_multiple(self):
        matches = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        )
        self.assertListEqual([("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")], matches)
        

if __name__ == "__main__":
    unittest.main()