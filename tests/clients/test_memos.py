from datetime import datetime
import unittest
from faker import Faker

from tests.test_base import BaseTest

class TestMemosClient(BaseTest):
    def setUp(self):
        super().setUp()
        self.client = self._get_memos_client()

if __name__ == '__main__':
    unittest.main()
