import os
import unittest
import yaml

from mastodon2memos.clients.memos import MemosClient
from mastodon2memos.clients.mastodon import MastodonClient

class BaseTest(unittest.TestCase):
    def setUp(self):
        config_path = os.path.join(os.path.dirname(__file__), '../config_test.yaml')
        with open(config_path, 'r') as file:
            self.config = yaml.safe_load(file)

    def _get_memos_client(self) -> MemosClient:
        return MemosClient(
            api_base_url=self.config['memos']['api_url'], 
            access_token=self.config['memos']['access_token']
        )

    def _get_mastodon_client(self) -> MastodonClient:
        return MastodonClient(
            api_base_url=self.config['mastodon']['api_url'],
            client_id=self.config['mastodon']['client_id'],
            client_secret=self.config['mastodon']['client_secret'],
            access_token=self.config['mastodon']['access_token']
        )

    def get_mastodon_username(self):
        return self.config['mastodon']['username']
