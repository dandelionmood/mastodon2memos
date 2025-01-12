import requests
import os
import base64
import mimetypes
import uuid

class MemosClient:
    def __init__(self, api_base_url: str, access_token: str) -> None:
        self.api_base_url = api_base_url
        self.access_token = access_token

    def _headers(self) -> dict:
        return {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json'
        }

    def create_memo(self, content: str, visibility: str = 'PUBLIC') -> dict:
        """
        Creates a new memo.

        :param content: Content of the memo.
        :param visibility: Visibility of the memo. Default is 'PUBLIC'.
        :return: dict: JSON response from the server.
        """
        url = f'{self.api_base_url}/api/v1/memos'
        payload = {
            'content': content,
            'visibility': visibility,
        }
        response = requests.post(url, headers=self._headers(), json=payload)
        response.raise_for_status()
        return response.json()

    def upload_resource(self, memo_name: str, file_path: str, external_link: str = '') -> dict:
        """
        Uploads a resource to the server.

        :param file_path: Path to the file to be uploaded.
        :param memo_name: The name the memo with which the resource is associated (i.e. "memo/1").
        :param external_link: Optional external link for the resource (e.g.: the toot URL)
        :return: dict: JSON response from the server.
        """
        url = f'{self.api_base_url}/api/v1/resources'
        with open(file_path, 'rb') as file:
            file_content = file.read()
            encoded_content = base64.b64encode(file_content).decode('utf-8')
            file_size = os.path.getsize(file_path)
            mime_type = mimetypes.guess_type(file_path)[0]
            payload = {
                'uid': str(uuid.uuid4()),
                'filename': os.path.basename(file_path),
                'content': encoded_content,
                'externalLink': external_link,
                'type': mime_type,
                'size': file_size,
                'memo': memo_name,
            }
            response = requests.post(url, headers=self._headers(), json=payload)
        response.raise_for_status()
        return response.json()
