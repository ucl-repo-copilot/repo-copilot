Here are the test cases for the functions and classes:

```python
import unittest
import tempfile
from file2 import parse_content, PolicySearch
import re
import uuid
from django.utils.html import escape

class TestParseContent(unittest.TestCase):
    def test_parse_content(self):
        with open('test.txt', 'w') as f:
            f.write("INFORMATION: This is some information SOURCE: https://www.test.com/information\n")
            f.write("INFORMATION: This is more information SOURCE: https://www.test2.com/more_info\n")

        content = ""
        with open('test.txt', 'r') as f:
            content = f.read()

        entries = parse_content(content)
        self.assertEqual(len(entries), 2)

        for entry in entries:
            self.assertIsInstance(entry['id'], str)
            self.assertIn('information', entry['information'].strip())
            self.assertIn('source', entry)

    def test_parse_content_empty(self):
        entries = parse_content("")
        self.assertEqual(len(entries), 0)


class TestPolicySearch(unittest.TestCase):

    def test_init(self):
        policy_search = PolicySearch()
        self.assertIsInstance(policy_search, object)


if __name__ == '__main__':
    unittest.main()

```