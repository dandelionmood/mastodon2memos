import unittest
import os
from faker import Faker

from tests.test_base import BaseTest 

class TestMemosClient(BaseTest):
    def setUp(self):
        super().setUp()
        self.client = self._get_memos_client()

    def test_create_memo(self):
        fake = Faker()
        content = fake.sentence(nb_words=10) + ' #' + fake.word() + ' #' + fake.word()
        response = self.client.create_memo(content)
        self.assertIn('name', response)
        self.assertIn('uid', response)
        self.assertIn('content', response)
        self.assertEqual(response['content'], content)

    def test_upload_resource(self):
        fake = Faker()
        content = fake.sentence(nb_words=10) + ' #' + fake.word() + ' #' + fake.word()
        response = self.client.create_memo(content)

        dir = os.path.dirname(__file__)
        testpic_path = os.path.join(dir, 'assets', 'testpic.png')
        response = self.client.upload_resource(
            file_path=testpic_path, 
            memo_name=response['name'], 
            external_link='https://www.example.com'
        )
        self.assertIn('uid', response)

if __name__ == '__main__':
    unittest.main()
