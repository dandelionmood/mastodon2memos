import unittest
import string
import random

from atproto.exceptions import AtProtocolError
from tests.test_base import BaseTest

class TestBlueskyClient(BaseTest):
    def setUp(self):
        super().setUp()

    def test_get_latest_posts(self):
        client = self._get_bluesky_client()
        
        # Get the user ID
        handle = self._get_bluesky_username()
        user_id = client.get_user_did_from_handle(handle)

        # Test with default count
        posts = client.get_latest_posts(user_id)
        self.assertGreaterEqual(len(posts), 0)  # Assuming there might be no posts
        if posts:
            self.assertIsInstance(posts[0].post.record.text, str)

        # Test exception handling
        with self.assertRaises(AtProtocolError):
            client.get_latest_posts('invalid_user_id')

    def test_get_user_did_from_handle(self):
        client = self._get_bluesky_client()
        handle = self._get_bluesky_username()

        # Test valid handle
        user_id = client.get_user_did_from_handle(handle)
        self.assertIsInstance(user_id, str)

        # Test invalid handle
        completely_random_handle = ''.join(random.choices(string.ascii_letters + string.digits, k=32))
        with self.assertRaises(AtProtocolError):
            client.get_user_did_from_handle(completely_random_handle)

if __name__ == '__main__':
    unittest.main()