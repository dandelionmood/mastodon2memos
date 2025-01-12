import os
import unittest
import yaml

from mastodon2memos.memos import MemosClient
from mastodon2memos.mastodon import MastodonClient

class BaseTest(unittest.TestCase):
    def setUp(self):
        config_path = os.path.join(os.path.dirname(__file__), '../config_test.yaml')
        with open(config_path, 'r') as file:
            self.config = yaml.safe_load(file)

    def _get_memos_client(self) -> MemosClient:
        return MemosClient(
            api_base_url=self.config['memos_api_base_url'], 
            access_token=self.config['memos_access_token']
        )

    def _get_mastodon_client(self) -> MastodonClient:
        return MastodonClient(
            api_base_url=self.config['api_base_url'],
            client_id=self.config['client_id'],
            client_secret=self.config['client_secret'],
            access_token=self.config['access_token']
        )
