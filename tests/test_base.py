import os
import unittest
import yaml

from mastodon2memos.clients.bluesky_client import BlueskyClient
from mastodon2memos.clients.memos_client import MemosClient
from mastodon2memos.clients.mastodon_client import MastodonClient

class BaseTest(unittest.TestCase):
    def setUp(self):
        # Load the test configuration
        config_path = os.path.join(os.path.dirname(__file__), '../config_test.yaml')
        with open(config_path, 'r') as file:
            self.config = yaml.safe_load(file)

    def _get_memos_client(self) -> MemosClient:
        """
        Get the Memos client.
        :return: The Memos client.
        """
        return MemosClient(
            api_base_url=self.config['memos']['api_url'], 
            access_token=self.config['memos']['access_token']
        )

    def _get_mastodon_client(self) -> MastodonClient:
        """
        Get the Mastodon client.
        :return: The Mastodon client
        """
        return MastodonClient(
            api_base_url=self.config['mastodon']['api_url'],
            client_id=self.config['mastodon']['client_id'],
            client_secret=self.config['mastodon']['client_secret'],
            access_token=self.config['mastodon']['access_token']
        )

    def _get_bluesky_client(self) -> BlueskyClient:
        """
        Get the Bluesky client.
        :return: The Bluesky client
        """
        return BlueskyClient(
            api_base_url=self.config['bluesky']['api_url'],
            handle=self.config['bluesky']['handle'], 
            password=self.config['bluesky']['password']
        )

    def _get_mastodon_username(self):
        """
        Get the Mastodon username from the config.
        """
        return self.config['mastodon']['username']
    
    def _get_bluesky_username(self):
        """
        Get the Bluesky username from the config.
        """
        return self.config['bluesky']['handle']