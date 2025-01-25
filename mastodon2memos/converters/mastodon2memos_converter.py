import html2text
from mastodon2memos import MASTODON2MEMOS_TAG, _
from mastodon2memos.clients.mastodon_client import MastodonClient
from mastodon2memos.clients.memos_client import MemosClient

class Mastodon2MemosConverter:
    """
    Mastodon2Memos Converter for converting Mastodon toots to Memos.
    """
    def __init__(self, memos_client: MemosClient, mastodon_client: MastodonClient):
        """
        Initialize the Mastodon2Memos Converter.
        :param memos_client: The Memos client.
        :param mastodon_client: The Mastodon client.
        """
        self.memos_client = memos_client
        self.mastodon_client = mastodon_client

    def publish_toot_as_memo(self, toot: dict) -> dict:
        """
        Publish a Mastodon toot as a Memo.
        :param toot: The Mastodon toot.
        :return: The Memo if successful.
        :raises RuntimeError: if the toot is already saved in memos.
        """

        if self.memos_client.find_by_toot_url(toot['url']):
            raise RuntimeError(_("Toot already saved in memos."))

        h = html2text.HTML2Text()
        h.ignore_links = True
        memo_content = h.handle(toot['content'])
        memo_content += _("> 🌐 [original toot]({url}) posted by [{acct}]({account_url}) #{tag}").format(
            url=toot['url'], 
            acct=toot['account']['acct'], 
            account_url=toot['account']['url'], 
            tag=MASTODON2MEMOS_TAG
        )

        # Create Memo
        memo = self.memos_client.create(memo_content)

        # Update Memo to update the creation date
        self.memos_client.update(memo['name'], toot['created_at'])

        # Upload media if any
        for attachment in toot['media_attachments']:
            self.memos_client.upload_resource(
                resource_url=attachment['url'],
                memo_name=memo['name'],
                created_at=toot['created_at']
            )
        
        return memo