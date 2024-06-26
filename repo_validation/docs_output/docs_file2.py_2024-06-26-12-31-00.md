Here are the test cases for the `PolicySearch` class and the `parse_content` function:

```
import unittest
from django.test import TestCase
from file2 import PolicySearch, parse_content


class TestPolicySearch(TestCase):
    def test_policy_search_attributes(self):
        policy = PolicySearch()
        self.assertEqual(policy.auto_increment_id, None)
        selfassertion(self.assertEqual(policy.created_at, None))
        self.assertIsString(policy.name, '')
        self.assertListEqual(list(policy.keywords.split(',')), [])
        selfassertion(self.assertEqual(policy.account, None))
        self.assertIsString(policy.object_id, '')
        selfassertion(self.assertEqual(policy.progress, 0))
        selfassertion(self.assertEqual(policy.unique_thread_id, ''))


class TestParseContent(TestCase):
    def test_parse_content_with_entries(self):
        content = "INFORMATION: Example INFORMATION: SOURCE: https://test.com/page INFORMATION: Another INFO"
        entries = parse_content(content)
        self.assertListEqual(entries, [
            {'information': 'Example', 'source': 'https://test.com/page', 'domain': 'https://test.com', 'id': uuid.uuid4()},
            {'information': 'Another INFO', 'source': '', 'domain': 'Invalid URL or no source', 'id': str(uuid.uuid4())}
        ])

    def test_parse_content_without_entries(self):
        content = "This is just a random text"
        entries = parse_content(content)
        self.assertListEqual(entries, [])
```