Here are some test cases for your file:

```
import unittest
from unittest.mock import patch, MagicMock
from django.db.models.base import ModelBase
from django.db.models.query_utils import Q
from django.utils.translation import gettext_lazy as _

class TestPolicySearch(unittest.TestCase):
    def test_init(self):
        policy = PolicySearch()
        self.assertEqual(policy.auto_increment_id, None)
        self.assertEqual(policy.created_at, None)
        self.assertEqual(policy.name, "")
        self.assertEqual(policy.keywords, "")
        self.assertEqual(policy.account, None)
        self.assertEqual(policy.object_id, "")
        self.assertEqual(policy.progress, 0)
        self.assertEqual(policy.unique_thread_id, "")

    @patch('django.db.models.fields.related_descriptors.ManyToOneRel')
    def test_str(self, mre):
        account = MagicMock()
        account.email = 'test@example.com'
        policy = PolicySearch(account=account)
        self.assertEqual(str(policy), f"{policy.name} - {account.email} - 1970-01-01 00:00:00")

class TestParseContent(unittest.TestCase):
    @patch('re.compile')
    def test_parse_content(self, re_compile):
        content = """INFORMATION: test1 SOURCE: https://test.com/test
INFORMATION: test2 SOURCE: https://test2.com/test2"""
        pattern = re_compile().return_value
        expected_entries = [{'information': 'test1', 'source': 'https://test.com/test', 'domain': 'https://test.com:', 'id': '12345678-1234-1234-1234-123456789012'},
                            {'information': 'test2', 'source': 'https://test2.com/test2', 'domain': 'https://test2.com:', 'id': '98765432-8765-4321-4321-876543210987'}]

        with patch('urllib.parse.urlparse') as urlparse_mock:
            pattern.findall.return_value = [('test1 https://test.com/test', 'https://test.com/test'), ('test2 https://test2.com/test2', 'https://test2.com/test2')]
            result_entries = parse_content(content)
            self.assertEqual(result_entries, expected_entries)

if __name__ == '__main__':
    unittest.main()
```