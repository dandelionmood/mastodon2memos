from atproto import Client
from mastodon2memos import _

class BlueskyClient:
    def __init__(self, api_base_url, handle, password):
        """
        Initialize the Bluesky client.
        :param api_base_url: The base URL of the Bluesky instance.
        :param handle: The handle (username) for the Bluesky account.
        :param password: The password for the Bluesky account.
        """
        self.api_base_url = api_base_url
        self.client = Client()
        try:
            self.client.login(handle, password)
        except Exception as e:
            raise RuntimeError(_("Failed to log in to Bluesky: {e}").format(e=e))

    def test_connection(self) -> bool:
        """
        Test the connection to the Bluesky instance.
        This can't fail as the client is already initialized in the constructor.
        :return: True always.
        """
        return True

    def get_user_did_from_handle(self, handle: str) -> str:
        """
        Get the user DID from a given Bluesky handle.
        :param handle: The Bluesky handle.
        :return: The user DID.
        :raises RuntimeError: if the handle is not found.
        """
        try: 
            user = self.client.resolve_handle(handle)
            return user['did']
        except Exception as e:
            raise RuntimeError(_("Failed to fetch user DID: {e}").format(e=e))

    def get_latest_posts(self, user_did: str, limit=5) -> dict:
        """
        Get the latest posts from a given Bluesky user.
        :param user_did: The Bluesky user DID.
        :param limit: The number of posts to fetch (default is 5).
        :return: A list of posts.
        :raises RuntimeError: if fetching posts fails.
        """
        try:
            response = self.client.get_author_feed(actor=user_did, limit=limit)
            return response['feed']
        except Exception as e:
            raise RuntimeError(_("Failed to fetch posts: {e}").format(e=e))
        
    def get_post_url(self, post: dict) -> str:
        """
        Get the URL of a Bluesky post.
        :param post: The Bluesky post.
        :return: The URL of the post.
        """
        author_handle = post['author']['handle']
        post_id = post['uri'].split('/')[-1]
        return self.api_base_url + "/profile/{author_handle}/post/{post_id}".format(
            author_handle=author_handle, 
            post_id=post_id)