from mastodon import Mastodon
from mastodon2memos import _

class MastodonClient:
    def __init__(self, api_base_url, client_id, client_secret, access_token):
        """
        Initialize the Mastodon client.
        :param api_base_url: The base URL of the Mastodon instance.
        :param client_id: The client ID for the Mastodon instance.
        :param client_secret: The client secret for the Mastodon instance.
        :param access_token: The access token for the Mastodon instance.
        :throws MastodonError if an error occurs.
        """
        self.mastodon = Mastodon(
            client_id=client_id,
            client_secret=client_secret,
            access_token=access_token,
            api_base_url=api_base_url
        )

    def get_user_id_from_username(self, username: str) -> int:
        """
        Get the user ID from a given Mastodon username.
        :param username: The Mastodon username.
        :throws MastodonNotFoundError if the username is not found
        :return: The user ID.
        """
        account = self.mastodon.account_lookup(username)
        return account['id']

    def get_latest_public_toots(self, user_id, count=5) -> list:
        """
        Get the latest public toots from a given Mastodon user (excluding reblogs & replies).
        :param user_id: The Mastodon user ID.
        :param count: The number of toots to fetch (default is 5).
        :throws MastodonError if an error occurs.
        :return: A list of toots.
        """
        # Fetch the latest public toots from the user excluding reblogs and replies
        return self.mastodon.account_statuses(user_id, limit=count, exclude_reblogs=True, exclude_replies=True)