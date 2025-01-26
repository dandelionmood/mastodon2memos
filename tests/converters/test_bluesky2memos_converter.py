from datetime import datetime
import unittest
from faker import Faker

from mastodon2memos.converters.bluesky2memos_converter import Bluesky2Memos_Converter
from tests.test_base import BaseTest

class TestBluesky2Memos_Convert(BaseTest):
    def setUp(self):
        super().setUp()
        self.converter = Bluesky2Memos_Converter(
            memos_client=self._get_memos_client(),
            bluesky_client=self._get_bluesky_client() 
        ) 
        
    def test_publish_bluesky_post_as_memo(self):
        """Test publishing a fabricated Bluesky post as a memo."""
        post = self._create_fake_bluesky_post()
        memo_content = self.converter.publish_post_as_memo(post)
        assert memo_content is not None

    def test_publish_bluesky_post_as_memo_already_saved(self):
        """Test publishing a Bluesky post that has already been saved as a memo."""
        post_uri = self._get_fake_bluesky_post_uri()
        
        # Create a memo with the known URL should work
        post = self._create_fake_bluesky_post(uri=post_uri)        
        result = self.converter.publish_post_as_memo(post)
        assert result is not None
        
        # Attempt to publish the same post again should raise an error
        with self.assertRaises(RuntimeError):
            self.converter.publish_post_as_memo(post)

    def _create_fake_bluesky_post(self, uri=None):
        """
        Helper method to create a fake Bluesky post.
        :param uri: The URI of the post.
        :return: A fake Bluesky post.
        """
        fake = Faker()
        return {
            'uri': uri if uri else self._get_fake_bluesky_post_uri(),
            'cid': fake.uuid4(),
            'author': {
                'did': fake.uuid4(),
                'handle': fake.user_name() + ".bsky.social",
                'displayName': fake.name(),
                'avatar': fake.image_url(),
                'createdAt': datetime.now().astimezone()
            },
            'record': {
                'text': "<br />".join(fake.sentences(nb=3))
            },
            'indexedAt': datetime.now().astimezone(),
            'embed': {
                'images': [
                    {
                        'value': "https://picsum.photos/640/480.jpg"
                    },
                    {
                        'value': "https://picsum.photos/480/640.jpg"
                    }                    
                ],
                # note: no video for now, unsure how this is implemented
            }
        }

    def _get_fake_bluesky_post_uri(self):
        """
        Helper method to generate a fake Bluesky post URI.
        :return: A fake Bluesky post URI.
        """
        fake = Faker()
        return f"at://did:plc:{fake.uuid4()}/app.bsky.feed.post/{fake.uuid4()}"

if __name__ == '__main__':
    unittest.main()
