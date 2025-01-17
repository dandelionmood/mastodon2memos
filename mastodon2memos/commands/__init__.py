import os
import yaml
import click
from mastodon2memos import _

from mastodon2memos.clients.mastodon_client import MastodonClient
from mastodon2memos.clients.memos_client import MemosClient

def validate_and_read_config(config_path):
    """
    Validate and read the configuration file.
    :param config_path: Path to the configuration file.
    :return: Configuration dictionary.
    """
    if not os.path.exists(config_path):
        click.echo(_('Configuration file not found at {config_path}. Please ensure the file exists.').format(config_path=config_path))
        exit(1)

    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)

    expected_keys = {
        'mastodon': ['api_url', 'client_id', 'client_secret', 'access_token', 'username'],
        'memos': ['api_url', 'access_token']
    }

    for section, keys in expected_keys.items():
        if section not in config:
            click.echo(_('Missing section "{section}" in configuration file.').format(section=section))
            exit(1)
        for key in keys:
            if key not in config[section]:
                click.echo(_('Missing key "{key}" in section "{section}" of configuration file.').format(key=key, section=section))
                exit(1)

    return config

def initialize_clients(config, report_success):
    """
    Initialize Mastodon and Memos clients.
    :param config: Configuration dictionary.
    :param report_success: Boolean to report success.
    :return: Tuple of MastodonClient and MemosClient.
    """
    mastodon_client = MastodonClient(
        api_base_url=config['mastodon']['api_url'],
        client_id=config['mastodon']['client_id'],
        client_secret=config['mastodon']['client_secret'],
        access_token=config['mastodon']['access_token']
    )
    memos_client = MemosClient(
        api_base_url=config['memos']['api_url'],
        access_token=config['memos']['access_token']
    )

    # Test Mastodon connection
    mastodon_status = mastodon_client.test_connection()
    if mastodon_status:
        if report_success:
            click.echo(_('Successfully connected to Mastodon API.'))
    else:
        click.echo(_('Failed to connect to Mastodon API.'))
        exit(1)

    # Test Memos connection
    memos_status = memos_client.test_connection()
    if memos_status:
        if report_success:
            click.echo(_('Successfully connected to Memos API.'))
    else:
        click.echo(_('Failed to connect to Memos API.'))
        exit(1)

    return mastodon_client, memos_client
