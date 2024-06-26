```
import unittest
from unittest.mock import patch, Mock
import pandas as pd
import re
import uuid
from file1 import parse_content
from django.shortcuts import render, redirect

class TestParseContent(unittest.TestCase):
    def test_parse_content(self):
        with patch('re.compile') as mock_compile:
            content = "INFORMATION: Test 1 SOURCE: https://test.com INFORMATION: Test 2 SOURCE: https://example.com"
            expected_result = [
                {
                    'information': 'Test 1',
                    'source': 'https://test.com',
                    'domain': 'https://test.com',
                    'id': str(uuid.uuid4())
                },
                {
                    'information': 'Test 2',
                    'source': 'https://example.com',
                    'domain': 'https://example.com',
                    'id': str(uuid.uuid4())
                }
            ]
            parse_content(content)
            self.assertEqual(mock_compile.return_value.findall.call_args_list, [(content,)])

if __name__ == '__main__':
    unittest.main()
```