Here are the test cases for the `parse_content` function:

```
import unittest
from file1 import parse_content
import re
from urllib.parse import urlparse
from uuid import UUID

class TestParseContent(unittest.TestCase):

    def test_parse_content(self):
        content = """
INFORMATION: Example information 1 
SOURCE: https://example.com/source1 INFORMATION: Example information 2 
SOURCE: https://example.net/source2
"""
        expected_output = [
            {
                'information': "Example information 1",
                'source': "https://example.com/source1",
                'domain': "https://example.com/",
                'id': UUID('12345678-1234-1234-1234-123456789012').hex
            },
            {
                'information': "Example information 2",
                'source': "https://example.net/source2",
                'domain': "https://example.net/",
                'id': UUID('23456789-8901-2345-6789-901234567890').hex
            }
        ]
        self.assertEqual(parse_content(content), expected_output)

if __name__ == '__main__':
    unittest.main()
```