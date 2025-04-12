import unittest

from markdown_html import markdown_to_html_node


class TestInlineMarkdown(unittest.TestCase):
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_headings(self):
        md = """
# heading 1

## heading 2

### heading 3

#### heading 4

##### heading 5

###### heading 6

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div>"+
            "<h1>heading 1</h1><h2>heading 2</h2>"+
            "<h3>heading 3</h3><h4>heading 4</h4>"+
            "<h5>heading 5</h5><h6>heading 6</h6>"+
            "</div>",
        )
    

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff</code></pre></div>",
        )

    def test_quote(self):
        md = """
> this is
> a quote

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>this is\na quote\n</blockquote></div>",
        )

    def test_ul(self):
        md = """
- this is
- a unordered list

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>this is</li><li>a unordered list</li></ul></div>",
        )

    def test_ol(self):
        md = """
1. this is
2. a ordered list

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>this is</li><li>a ordered list</li></ol></div>",
        )
        

if __name__ == "__main__":
    unittest.main()