import os
import yaml
from mastodon2memos import _

from mastodon2memos.clients.mastodon_client import MastodonClient
from mastodon2memos.clients.memos_client import MemosClient
from mastodon2memos.clients.bluesky_client import BlueskyClient

def validate_and_read_config(config_path):
    """
    Validate and read the configuration file.
    :param config_path: Path to the configuration file.
    :return: Configuration dictionary.
    :raises Exception if the configuration is invalid or missing
    """
    if not os.path.exists(config_path):
        raise Exception(_('Configuration file not found at {config_path}. Please ensure the file exists.').format(config_path=config_path))

    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)

    expected_keys = {
        'mastodon': ['api_url', 'client_id', 'client_secret', 'access_token', 'username', 'enabled'],
        'memos': ['api_url', 'access_token'],
        'bluesky': ['api_url', 'handle', 'password', 'enabled']
    }

    for section, keys in expected_keys.items():
        if section not in config:
            raise Exception(_('Missing section "{section}" in configuration file.').format(section=section))
        for key in keys:
            if key not in config[section]:
                raise Exception(_('Missing key "{key}" in section "{section}" of configuration file.').format(key=key, section=section))

    return config

def initialize_mastodon_client(config):
    """
    Initialize Mastodon client.
    :param config: Configuration dictionary.
    :return: Initialized Mastodon client
    :raises Exception if the connection fails
    """
    mastodon_client = MastodonClient(
        api_base_url=config['mastodon']['api_url'],
        client_id=config['mastodon']['client_id'],
        client_secret=config['mastodon']['client_secret'],
        access_token=config['mastodon']['access_token']
    )
    # Test Mastodon connection
    if not mastodon_client.test_connection():
        raise Exception(_('Failed to connect to Mastodon API.'))
    return mastodon_client

def initialize_memos_client(config):
    """
    Initialize Memos client.
    :param config: Configuration dictionary.
    :return: Initialized Memos client.
    :raises Exception if the connection fails
    """
    memos_client = MemosClient(
        api_base_url=config['memos']['api_url'],
        access_token=config['memos']['access_token']
    )
    # Test Memos connection
    if not memos_client.test_connection():
        raise Exception(_('Failed to connect to Memos API.'))
    return memos_client

def initialize_bluesky_client(config):
    """
    Initialize Bluesky client.
    :param config: Configuration dictionary.
    :return: Initialized Bluesky client
    :raises Exception if the connection fails
    """
    bluesky_client = BlueskyClient(
        api_base_url=config['bluesky']['api_url'],
        handle=config['bluesky']['handle'],
        password=config['bluesky']['password']
    )
    # Test Bluesky connection
    if not bluesky_client.test_connection():
        raise Exception(_('Failed to connect to Bluesky API.'))
    return bluesky_client

def is_mastodon_enabled(config: dict):
    """
    Check if the Mastodon connection is enabled in the configuration.
    :param config: Configuration dictionary.
    :return: bool: True if Mastodon is enabled, False otherwise.
    """
    return config.get('mastodon', {}).get('enabled', False)

def is_bluesky_enabled(config: dict):
    """
    Check if the Bluesky connection is enabled in the configuration.
    :param config: Configuration dictionary.
    :return: bool: True if Bluesky is enabled, False otherwise.
    """
    return config.get('bluesky', {}).get('enabled', False)