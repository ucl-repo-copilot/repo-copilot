```
import unittest
from unittest.mock import patch, MagicMock
from file1 import parse_content

class TestParseContent(unittest.TestCase):
    @patch('re.compile')
    def test_parse_content(self, compile_mock):
        mock_pattern = MagicMock()
        mock_pattern.findall.side_effect = [
            [('Information 1', 'Source 1'), ('Information 2', 'Source 2')], 
            [], 
            [('Information 3', 'Source 3')]
        ]
        
        parse_content('Content 1\nINFORMATION: Information 1\nSOURCE: Source 1\nINFORMATION: Information 2\nSOURCE: Source 2')
        self.assertEqual(len(mock_pattern.findall.call_args_list), 3)

    @patch('re.compile')
    def test_parse_empty_string(self, compile_mock):
        parse_content('')
        self.assertEqual(len(compile_mock().findall.return_value), 0)

    @patch('re.compile')
    def test_parse_single_entry(self, compile_mock):
        mock_pattern = MagicMock()
        mock_pattern.findall.return_value = [('Information', 'Source')]
        
        entries = parse_content('Content\nINFORMATION: Information\nSOURCE: Source')
        self.assertEqual(len(entries), 1)
        self.assertEqual(entries[0]['information'], 'Information')

    @patch('re.compile')
    def test_parse_no_matches(self, compile_mock):
        mock_pattern = MagicMock()
        mock_pattern.findall.return_value = []
        
        entries = parse_content('No matches here\nINFORMATION: No information\nSOURCE: No source')
        self.assertEqual(len(entries), 0)

if __name__ == '__main__':
    unittest.main()
```