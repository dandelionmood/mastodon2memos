from datetime import datetime
import unittest
from faker import Faker

from tests.test_base import BaseTest

class TestMemosClient(BaseTest):
    def setUp(self):
        super().setUp()
        self.client = self._get_memos_client()

    def test_connection(self):
        """Test the connection to the Memos API."""
        response = self.client.test_connection()
        assert response is True

if __name__ == '__main__':
    unittest.main()
