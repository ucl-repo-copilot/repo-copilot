Here are the test cases:

```
import unittest
from django.test import TestCase
from file2 import PolicySearch, parse_content


class TestPolicySearch(TestCase):
    def setUp(self):
        self.policy_search = PolicySearch()

    def test_policy_search_str_representation(self):
        self.assertEqual(str(self.policy_search), " -  - ")

    def test_policy_search_auto_increment_id_set(self):
        self.assertEqual(self.policy_search.auto_increment_id, None)

    def test_policy_search_account_set(self):
        account = Account()
        self.policy_search.account = account
        self.assertEqual(self.policy_search.account, account)


class TestParseContent(unittest.TestCase):

    def setUp(self):
        self.content = """
INFORMATION: This is information
SOURCE: https://example.com
INFORMATION: Another piece of information
SOURCE: http://www.example.org

"""

    def test_parse_content(self):
        result = parse_content(self.content)
        expected_output = [
            {'information': 'This is information', 'source': 'https://example.com', 'domain': 'https://example.com/', 'id': str(uuid.uuid4())},
            {'information': 'Another piece of information', 'source': 'http://www.example.org', 'domain': 'http://www.example.org/', 'id': str(uuid.uuid4())}
        ]
        self.assertEqual(result, expected_output)


if __name__ == '__main__':
    unittest.main()
```