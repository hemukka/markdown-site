import unittest

from main import extract_title

class TestMain(unittest.TestCase):
    def test_extract_title(self):
        md = """
# heading is here

paragraph
"""
        heading = extract_title(md)
        self.assertEqual(
            heading,
            "heading is here"
        )

    def test_extract_title_not(self):
        md = """
## no h1 headings here

"""
        with self.assertRaises(Exception):
            extract_title(md)
        

if __name__ == "__main__":
    unittest.main()