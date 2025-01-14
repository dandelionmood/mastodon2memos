import unittest
import string
import random

from mastodon import MastodonNotFoundError

from tests.test_base import BaseTest 

class TestMastodonClient(BaseTest):
    def setUp(self):
        super().setUp()

    def test_get_latest_public_toots(self):
        client = self._get_mastodon_client()
        username = self.get_mastodon_username()
        user_id = client.get_user_id_from_username(username)

        # Test with default count
        toots = client.get_latest_public_toots(user_id)
        self.assertGreaterEqual(len(toots), 0)  # Assuming there might be no toots
        if toots:
            self.assertIn('content', toots[0])

        # Test with custom count
        toots = client.get_latest_public_toots(user_id, count=3)
        self.assertGreaterEqual(len(toots), 0)
        if toots:
            self.assertIn('content', toots[0])

        # Test exception handling
        with self.assertRaises(RuntimeError):
            client.get_latest_public_toots('invalid_user_id')

    def test_get_user_id_from_username(self):
        client = self._get_mastodon_client()
        username = self.get_mastodon_username()

        # Test valid username
        user_id = client.get_user_id_from_username(username)
        self.assertIsInstance(user_id, int)

        # Test invalid username
        completely_random_username = ''.join(random.choices(string.ascii_letters + string.digits, k=32))
        with self.assertRaises(MastodonNotFoundError):
            client.get_user_id_from_username(completely_random_username)

    def test_connection(self):
        client = self._get_mastodon_client()
        
        # Test successful connection
        self.assertTrue(client.test_connection())

if __name__ == '__main__':
    unittest.main()
