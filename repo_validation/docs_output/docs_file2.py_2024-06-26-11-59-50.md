```
import unittest
from django.test import TestCase
from django.db.models.functions import AutoField
from .file2 import PolicySearch, parse_content


class TestPolicySearch(TestCase):
    def test_policy_search(self):
        policy_search = PolicySearch()
        self.assertIsInstance(policy_search.auto_increment_id, AutoField)
        self.assertEqual(policy_search.name, "")
        self.assertEqual(policy_search.keywords, "")
        self.assertFalse(policy_search.account is None)
        self.assertEqual(policy_search.object_id, "")
        self.assertEqual(policy_search.progress, 0)
        self.assertEqual(policy_search.unique_thread_id, "")


class TestParseContent(unittest.TestCase):
    def test_parse_content(self):
        content = "INFORMATION: Something1 SOURCE: http://test.com INFORMATION: Something2 SOURCE: https://test.io\n" \
                  "INFORMATION: Information3 SOURCE: http://test.com"
        result = parse_content(content)
        self.assertEqual(len(result), 2)
        for entry in result:
            self.assertIn('information', entry)
            self.assertIn('source', entry)
            self.assertIn('domain', entry)
            self.assertIn('id', entry)


if __name__ == '__main__':
    unittest.main()
```