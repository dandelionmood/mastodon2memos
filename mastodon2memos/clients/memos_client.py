from datetime import datetime
import requests
import os
import base64
import mimetypes
import uuid
import tempfile
from mastodon2memos import MASTODON2MEMOS_TAG, _

class MemosClient:
    """
    Memos Client for interacting with the Memos API.
    """
    
    def __init__(self, api_base_url: str, access_token: str) -> None:
        """
        Initialize the Memos client.
        :param api_base_url: The base URL of the Memos API.
        :param access_token: The access token for the Memos API.
        """
        self.api_base_url = api_base_url
        self.access_token = access_token

    def create(self, content: str, visibility: str = 'PUBLIC') -> dict:
        """
        Creates a new memo.

        :param content: Content of the memo.
        :param visibility: Visibility of the memo. Default is 'PUBLIC'.
        :return: dict: JSON response from the server.
        :raises HTTPError: if the request to create the memo fails.
        """
        url = f'{self.api_base_url}/api/v1/memos'
        payload = {
            'content': content,
            'visibility': visibility,
        }
        response = requests.post(url, headers=self._headers(), json=payload)
        response.raise_for_status()
        return response.json()

    def update(self, memo_name: str, created_at: datetime) -> None:
        """
        Updates the memo's createTime, updateTime & displayTime with the post's created_at date.
        This ensures that the memo's date is consistent with the post's date.

        :param memo_id: The ID of the memo to update.
        :param created_at: The created_at date from the post.
        :raises HTTPError: if the request to update the memo fails.
        """
        url = f'{self.api_base_url}/api/v1/{memo_name}'
        created_at_rfc3339 = created_at.isoformat()
        payload = {
            'createTime': created_at_rfc3339,
            'displayTime': created_at_rfc3339,
            'updateTime': created_at_rfc3339,
        }
        response = requests.patch(url, headers=self._headers(), json=payload)
        response.raise_for_status()
        return response.json()

    def upload_resource(self, memo_name: str, resource_url: str, created_at: datetime) -> dict:
        """
        Uploads a resource to the server.

        :param memo_name: The name the memo with which the resource is associated (i.e. "memo/1").
        :param resource_url: The URL of the resource.
        :param created_at: The created_at date from the post.
        :return: dict: JSON response from the server.
        :raises HTTPError: if the request to upload the resource fails.
        """
        # Download the file from resource_url to a temporary location
        response = requests.get(resource_url)
        response.raise_for_status()
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(resource_url)[1]) as temp_file:
            temp_file.write(response.content)
            file_path = temp_file.name

        # Open the file and read the content 
        with open(file_path, 'rb') as file:
            # Encode the file content to base64
            file_content = file.read()
            encoded_content = base64.b64encode(file_content).decode('utf-8')
            file_size = os.path.getsize(file_path)
            mime_type = mimetypes.guess_type(file_path)[0]
            
            # Upload the resource to the server
            url = f'{self.api_base_url}/api/v1/resources'
            payload = {
                'uid': str(uuid.uuid4()),
                'filename': os.path.basename(file_path),
                'content': encoded_content,
                'externalLink': resource_url,
                'type': mime_type,
                'size': file_size,
                'memo': memo_name,
                'createTime': created_at.isoformat(),
            }
            response = requests.post(url, headers=self._headers(), json=payload)
        response.raise_for_status()
        return response.json()

    def get_memo_url(self, memo_name: str) -> str:
        """
        Get the URL of a memo.

        :param memo_uid: The UID of the memo.
        :return: str: The URL of the memo.
        """
        # extract ID from the name (e.g. memos/oDg8LyYMkBXJ4ekJc3ejo5)
        memo_id = memo_name.split('/')[-1]

        # Get the memo URL using the uid field value and the base URL
        return f'{self.api_base_url}/m/{memo_id}'

    def find_by_toot_url(self, toot_url: str) -> dict:
        """
        Check if a Mastodon toot is already a Memo.

        :param toot_url: The URL of the toot.
        :return: dict: The memo object if the toot is already a Memo, None otherwise.
        :raises HTTPError: if the request to find the memo fails.
        """
        url = f'{self.api_base_url}/api/v1/memos'
        params = {
            # CEL formated seach query
            # See here for more info: https://github.com/usememos/dotcom/blob/main/content/docs/getting-started/shortcuts.md
            'filter': f'tag in ["{MASTODON2MEMOS_TAG}"] && content.contains(\"{toot_url}\")',
            'pageSize': 1
        }
        response = requests.get(url, headers=self._headers(), params=params)
        response.raise_for_status()
        memos = response.json()
        # Return the first memo if it exists, None otherwise
        return memos['memos'][0] if memos and len(memos['memos']) > 0 else None

    # Alias for find_by_toot_url, for clarity and potential future changes.
    find_by_bluesky_post_url = find_by_toot_url
    
    def _headers(self) -> dict:
        """
        Returns the headers for the API requests.
        :return: dict: The headers.
        """
        return {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json',
        }