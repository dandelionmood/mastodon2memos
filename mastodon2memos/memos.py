import html2text
import requests
import os
import base64
import mimetypes
import uuid
import tempfile

class MemosClient:
    """
    Tag used to identify memos created by this script.
    """
    MASTODON2MEMOS_TAG = 'mastodon2memos'
    
    def __init__(self, api_base_url: str, access_token: str) -> None:
        """
        Initialize the Memos client.
        :param api_base_url: The base URL of the Memos API.
        :param access_token: The access token for the Memos API.
        """
        self.api_base_url = api_base_url
        self.access_token = access_token

    def publish_toot_as_memo(self, toot: dict) -> dict:
        """
        Publish a toot as a memo on Memos.
        :param toot: A Mastodon toot object.
        """
        # Check if the toot has already been saved as a memo using the URL
        # See in the signature of the memo content how we add the toot URL
        if self._is_toot_already_a_memo(toot['url']):
            return None

        # Convert HTML content to Markdown
        h = html2text.HTML2Text()
        h.ignore_links = True
        memo_content = h.handle(toot['content'])
        
        # Adding a signature to the content with notably the original toot URL
        # This is very important as we will use this signature to check if the toot has already been saved as a memo
        memo_content += f"> 🌐 [Original Toot]({toot['url']}) posted by [{toot['account']['acct']}]({toot['account']['url']}) #{self.MASTODON2MEMOS_TAG}"

        # Create a memo with the toot content
        memo = self._create_memo(memo_content)
        
        # Update the created memo with toot original date to ensure consistency
        self._update_memo(memo['name'], toot['created_at'])
        
        # Check if the toot has media attachments
        for attachment in toot['media_attachments']:
            media_url = attachment['url']
            # Extract the file extension
            file_extension = os.path.splitext(media_url)[1]
            # Download the media file
            media_response = requests.get(media_url)
            with tempfile.NamedTemporaryFile(delete=False, suffix=file_extension) as temp_file:
                temp_file.write(media_response.content)
                media_file_path = temp_file.name
                temp_file.close()

            # Upload the media file to Memos
            self._upload_resource(
                file_path=media_file_path,
                memo_name=memo['name'],
                external_link=media_url
            )

            # Remove media_file_path file
            os.unlink(media_file_path)
        
        # Return the memo object
        return memo
    
    def test_connection(self) -> bool:
        """
        Test the connection to the Memos API by getting the authentication status.
        :return: bool: True if the connection is successful, False otherwise.
        """
        url = f'{self.api_base_url}/api/v1/auth/status'
        response = requests.post(url, headers=self._headers())
        response.raise_for_status()
        return response.json()['id'] is not None

    def _is_toot_already_a_memo(self, toot_url: str) -> bool:
        """
        Checks if a toot is already published as a memo (using its unique URL as a differenciator).
        :param toot_url: The URL of the toot.
        :return: bool: True if the toot is already a memo, False otherwise.
        """
        url = f'{self.api_base_url}/api/v1/memos'
        params = {
            # Filter by our mastodon2memos tag and content search to find the memo with the toot URL
            'filter': f'tag_search == ["{self.MASTODON2MEMOS_TAG}"] && content_search == ["]({toot_url})"]',
            # There's only one memo to find
            'pageSize': 1
        }
        response = requests.get(url, headers=self._headers(), params=params)
        response.raise_for_status()
        memos = response.json()
        return len(memos['memos']) > 0 if memos else False

    def _headers(self) -> dict:
        """
        Returns the headers for the API requests.
        """
        return {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json'
        }

    def _create_memo(self, content: str, visibility: str = 'PUBLIC') -> dict:
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

    def _update_memo(self, memo_name: str, created_at) -> None:
        """
        Updates the memo's createTime, updateTime & displayTime with the toot's created_at date.
        This ensures that the memo's date is consistent with the toot's date.

        :param memo_id: The ID of the memo to update.
        :param created_at: The created_at date from the toot.
        """
        url = f'{self.api_base_url}/api/v1/{memo_name}'
        payload = {
            'createTime': created_at.isoformat(),
            'displayTime': created_at.isoformat(),
            'updateTime': created_at.isoformat(),
        }
        response = requests.patch(url, headers=self._headers(), json=payload)
        response.raise_for_status()

    def _upload_resource(self, memo_name: str, file_path: str, external_link: str = '') -> dict:
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
