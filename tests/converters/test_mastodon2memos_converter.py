from datetime import datetime
import unittest
from faker import Faker

from mastodon2memos.converters.mastodon2memos_converter import Mastodon2MemosConverter
from tests.test_base import BaseTest

class TestMastodon2Memos_Converter(BaseTest):
    def setUp(self):
        super().setUp()
        self.converter = Mastodon2MemosConverter(
            memos_client=self._get_memos_client(),
            mastodon_client=self._get_mastodon_client() 
        ) 

    def test_publish_toot_as_memo(self):
        """Test publishing a fabricated toot as a memo."""
        toot = self._create_fake_toot()
        memo_content = self.converter.publish_toot_as_memo(toot)
        assert memo_content is not None

    def test_publish_toot_as_memo_already_saved(self):
        """Test publishing a toot that has already been saved as a memo."""
        fake = Faker()
        toot_url = fake.url()
        
        # Create a memo with the known URL should work
        toot = self._create_fake_toot(url=toot_url)
        result = self.converter.publish_toot_as_memo(toot)
        assert result is not None
        
        # Attempt to publish the same toot again should raise an error
        with self.assertRaises(RuntimeError):
            self.converter.publish_toot_as_memo(toot)

    def _create_fake_toot(self, url=None):
        """
        Helper method to create a fake toot.
        :param url: The URL of the toot.
        """
        fake = Faker()
        return {
            'content': "<br />".join(fake.sentences(nb=3)),
            'created_at': datetime.now().astimezone(),
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
                },
                # Enable this to test video attachments, should work 
                # out of the box with the current implementation    
                #{
                #    'url': "https://ia802803.us.archive.org/15/items/nwmbc-Lorem_ipsum_video_-_Dummy_video_for_your_website/Lorem_ipsum_video_-_Dummy_video_for_your_website.mp4"
                #}
            ]
        }

if __name__ == '__main__':
    unittest.main()
