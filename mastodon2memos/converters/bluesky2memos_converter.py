from datetime import datetime
import html2text
from mastodon2memos import MASTODON2MEMOS_TAG, _
from mastodon2memos.clients.bluesky_client import BlueskyClient
from mastodon2memos.clients.memos_client import MemosClient

class Bluesky2Memos_Converter:
    """
    Bluesky2Memos Converter for converting Bluesky posts to Memos.
    """
    def __init__(self, memos_client: MemosClient, bluesky_client: BlueskyClient):
        """
        Initialize the Bluesky2Memos Converter.
        :param memos_client: The Memos client.
        :param bluesky_client: The Bluesky client.
        """
        self.memos_client = memos_client
        self.bluesky_client = bluesky_client

    def publish_post_as_memo(self, post: dict) -> dict:
        """
        Publish a Bluesky post as a Memo.
        :param post: The Bluesky post.
        :return: The Memo if successful.
        :raises RuntimeError: if the post is already saved in memos.
        """
        post_url = self.bluesky_client.get_post_url(post)
        if self.memos_client.find_by_bluesky_post_url(post_url):
            raise RuntimeError(_("Post already saved in memos."))

        h = html2text.HTML2Text()
        h.ignore_links = True
        memo_content = h.handle(post.record.text)
        memo_content += _("> 🌐 [original bluesky post]({url}) posted by [{acct}]({account_url}) #{tag}").format(
            url=post_url, 
            acct=post.author.handle,
            account_url="https://"+post.author.handle,
            tag=MASTODON2MEMOS_TAG)
        
        # Create Memo
        memo = self.memos_client.create(memo_content)

        created_at = datetime.fromisoformat(post.record.created_at)
        # Update Memo to update the creation date
        self.memos_client.update(memo['name'], created_at)

        # Test for existence of embed and images which may not exist 
        if hasattr(post, 'embed') and hasattr(post.embed, 'images'):

            # Upload images if any, video unsupported for now
            for image in post.record.embed.images:
                # Get the image URL from the known DID and IPLD link
                did = post.author.did
                ipld_link = image.image.ref.link 

                # We add the "?.jpg" extension to the image URL to ensure that Memos will display the image
                # This is not ideal, but it works for now
                image_url = f"https://cdn.bsky.app/img/feed_fullsize/plain/{did}/{ipld_link}@jpeg?.jpg"

                self.memos_client.upload_resource(
                    resource_url=image_url,
                    memo_name=memo['name'],
                    created_at=created_at
                )

        return memo
