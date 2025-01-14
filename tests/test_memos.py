from datetime import tzinfo, timezone, timedelta
import unittest
from faker import Faker

from tests.test_base import BaseTest 

class TestMemosClient(BaseTest):
    def setUp(self):
        super().setUp()
        self.client = self._get_memos_client()

    def test_publish_toot_as_memo(self):
        """Test publishing a fabricated toot as a memo."""
        toot = self._create_fake_toot()
        memo_content = self.client.publish_toot_as_memo(toot)
        assert memo_content is not None

    def test_publish_toot_as_memo_already_saved(self):
        """Test publishing a toot that has already been saved as a memo."""
        fake = Faker()
        toot_url = fake.url()
        
        # Create a memo with the known URL should work
        toot = self._create_fake_toot(url=toot_url)
        result = self.client.publish_toot_as_memo(toot)
        assert result is not None
        
        # Attempt to publish the same toot again should return None
        result = self.client.publish_toot_as_memo(toot)
        assert result is None

    def test_connection(self):
        """Test the connection to the Memos API."""
        response = self.client.test_connection()
        assert response is True

    def _create_fake_toot(self, url=None):
        """
        Helper method to create a fake toot.
        :param url: The URL of the
        """

        fake = Faker()
        return {
            'content': "<br />".join(fake.sentences(nb=3)),
            'created_at': fake.past_datetime(tzinfo=timezone(timedelta(hours=1))),
            'url': url if url else fake.url(),
            'account': {
                'acct': fake.user_name(),
                'url': fake.url()
            },
            'media_attachments': [
                {
                    'url': "https://picsum.photos/640/480.jpg"
                },
                {
                    'url': "https://picsum.photos/480/640.jpg"
                }
            ]
        }

if __name__ == '__main__':
    unittest.main()
