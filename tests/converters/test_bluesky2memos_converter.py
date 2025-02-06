from datetime import datetime
from types import SimpleNamespace
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
        return SimpleNamespace(
            uri=uri if uri else fake.uuid4(),
            cid=fake.uuid4(),
            author=SimpleNamespace(
                did=fake.uuid4(),
                handle=fake.user_name() + ".bsky.social",
                display_name=fake.name(),
                avatar=fake.image_url(),
                created_at=datetime.now().astimezone().strftime("%Y-%m-%dT%H:%M:%S.000Z")
            ),
            record=SimpleNamespace(
                text="<br />".join(fake.sentences(nb=3)),
                created_at=datetime.now().astimezone().strftime("%Y-%m-%dT%H:%M:%S.000Z")
            )
            # no embed
        )

    def _get_fake_bluesky_post_uri(self):
        """
        Helper method to generate a fake Bluesky post URI.
        :return: A fake Bluesky post URI.
        """
        fake = Faker()
        return f"at://did:plc:{fake.uuid4()}/app.bsky.feed.post/{fake.uuid4()}"

if __name__ == '__main__':
    unittest.main()
