import pprint
from mastodon import Mastodon, StreamListener
import requests
import html2text
from datetime import datetime

class MastodonClient:
    def __init__(self, api_base_url, client_id, client_secret, access_token):
        self.mastodon = Mastodon(
            client_id=client_id,
            client_secret=client_secret,
            access_token=access_token,
            api_base_url=api_base_url
        )
        # Check connection
        try:
            self.mastodon.account_verify_credentials()
        except Exception as e:
            raise ConnectionError(f"Failed to connect to Mastodon instance: {e}")

    def publish_new_toots_on_memos(self, memos_client):
        """Listen to toots from the Mastodon account and create matching memos in the Memos instance."""
        self.mastodon.stream_user(MastodonClientListener(memos_client))

class MastodonClientListener(StreamListener):
    def __init__(self, memos_client):
        self.memos_client = memos_client

    def on_update(self, status):
        """Called when a new toot is received."""
        pprint.pprint(status)

        # Convert HTML content to Markdown
        h = html2text.HTML2Text()
        h.ignore_links = False
        memo_content = h.handle(status['content'])
        
        # Format the created_at timestamp
        formatted_created_at = status['created_at'].strftime('%Y-%m-%d %H:%M:%S')

        # Adding a signature with the original toot URL
        memo_content += f"\n\n🌐 [Original Toot]({status['url']}) posted by [{status['account']['acct']}]({status['account']['url']}) at {formatted_created_at} #mastodon2memos"

        pprint.pprint(memo_content)

        # Create a memo with the toot content
        memo = self.memos_client.create_memo(memo_content)
        
        # Check if the toot has media attachments
        for attachment in status['media_attachments']:
            media_url = attachment['url']
            media_extension = media_url.split('.')[-1]
            # Download the media file
            media_response = requests.get(media_url)
            media_file_path = f'/tmp/media.{media_extension}'
            with open(media_file_path, 'wb') as media_file:
                media_file.write(media_response.content)

            # Upload the media file to Memos
            self.memos_client.upload_resource(
                file_path=media_file_path,
                memo_name=memo['name'],
                external_link=media_url
            )