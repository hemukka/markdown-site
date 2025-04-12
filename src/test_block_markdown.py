import unittest

from block_markdown import BlockType, markdown_to_blocks, block_to_block_type

class TestMarkdownBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
# This is a heading

  This is **bolded** paragraph with whitespace around    

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

Next comes multiple empty lines



- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "# This is a heading",
                "This is **bolded** paragraph with whitespace around",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "Next comes multiple empty lines",
                "- This is a list\n- with items",
            ],
        )

    def test_block_to_blocktype_h1(self):
        md_block = """# this is h1 heading"""
        block_type = block_to_block_type(md_block)
        self.assertEqual(block_type, BlockType.H)

    def test_block_to_blocktype_h6(self):
        md_block = """###### this is h6 heading"""
        block_type = block_to_block_type(md_block)
        self.assertEqual(block_type, BlockType.H)

    def test_block_to_blocktype_h7(self):
        md_block = """####### this is h7 heading, should become P"""
        block_type = block_to_block_type(md_block)
        self.assertEqual(block_type, BlockType.P)

    def test_block_to_blocktype_code_multiline(self):
        md_block = """```
        this is a code block
        def func
        ```"""
        block_type = block_to_block_type(md_block)
        self.assertEqual(block_type, BlockType.CODE)
    
    def test_block_to_blocktype_code_oneline(self):
        md_block = """```this is a code block```"""
        block_type = block_to_block_type(md_block)
        self.assertEqual(block_type, BlockType.CODE)

    def test_block_to_blocktype_code_not(self):
        md_block = """```
        this is a code block
        inproperly formatted at the end
        ```x"""
        block_type = block_to_block_type(md_block)
        self.assertEqual(block_type, BlockType.P)

    def test_block_to_blocktype_quote_oneline(self):
        md_block = """>quoting"""
        block_type = block_to_block_type(md_block)
        self.assertEqual(block_type, BlockType.QUOTE)

    def test_block_to_blocktype_quote_multiline(self):
        md_block = """>quoting
>
>asd"""
        block_type = block_to_block_type(md_block)
        self.assertEqual(block_type, BlockType.QUOTE)

    def test_block_to_blocktype_quote_multiline_not(self):
        md_block = """>quoting
missing >
>asd"""
        block_type = block_to_block_type(md_block)
        self.assertEqual(block_type, BlockType.P)

    def test_block_to_blocktype_ul_oneline(self):
        md_block = """- unordered list"""
        block_type = block_to_block_type(md_block)
        self.assertEqual(block_type, BlockType.UL)

    def test_block_to_blocktype_ul_oneline_not(self):
        md_block = """-ul without space after -"""
        block_type = block_to_block_type(md_block)
        self.assertEqual(block_type, BlockType.P)

    def test_block_to_blocktype_ol_multiline(self):
        md_block = """1. one
2. two
3. three"""
        block_type = block_to_block_type(md_block)
        self.assertEqual(block_type, BlockType.OL)

    def test_block_to_blocktype_ol_multiline_not(self):
        md_block = """1. one
2.two
3. three"""
        block_type = block_to_block_type(md_block)
        self.assertEqual(block_type, BlockType.P)

    def test_block_to_blocktype_ol_multiline_not_2(self):
        md_block = """1. one
3. two
4. three"""
        block_type = block_to_block_type(md_block)
        self.assertEqual(block_type, BlockType.P)

    def test_block_to_blocktype_ol_multiline_not_3(self):
        md_block = """1. one
2 two
3. three"""
        block_type = block_to_block_type(md_block)
        self.assertEqual(block_type, BlockType.P)

    def test_block_to_blocktype_p(self):
        md_block = """just a paragraph
        wiht few
        lines"""
        block_type = block_to_block_type(md_block)
        self.assertEqual(block_type, BlockType.P)

if __name__ == "__main__":
    unittest.main()