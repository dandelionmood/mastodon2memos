import pprint
import click
import yaml
import os

from mastodon2memos.mastodon import MastodonClient
from mastodon2memos.memos import MemosClient

@click.group()
def cli():
    """CLI tool for Mastodon to Memos operations."""
    pass

@click.command(name='mastodon2memos', 
               help='Publish Mastodon toots as Memos.')
@click.option('--interactive', is_flag=True, help='Ask before creating a new memo from a toot.')
@click.option('--config-path', default='config.yaml', help='Path to the configuration file.')
def mastodon2memos(interactive, config_path):
    """CLI tool to publish Mastodon toots as Memos."""

    # Validate and read the configuration file
    _validate_and_read_config(config_path)

    # Initialize the Mastodon and Memos clients
    _initialize_clients(report_success=False)

    # Get the user ID from the Mastodon username
    user_id = mastodon_client.get_user_id_from_username(config['mastodon']['username'])
    # Get the latest public toots
    new_toots = mastodon_client.get_latest_public_toots(user_id, count=30)  # Load 30 public toots
    # Attempt to publish each new toot as a memo
    for toot in new_toots:

        click.echo(f'---')
        click.echo(f'Processing toot: {toot["url"]}')

        if interactive:
            if not click.confirm(f'Do you want to attempt publishing this toot as a memo?\n{toot["content"]}\n{toot["url"]}?'):
                click.echo(f'Skipping toot.')
                continue
        memo = memos_client.publish_toot_as_memo(toot)  # Use publish_toot_as_memo method
        if memo:
            click.echo(f'New toot added to memos.')
        else:
            click.echo(f'No memo added, toot was already saved in memos.')

    click.echo('Finished processing toots.')
    return True

@click.command(name='troubleshoot', 
               help='Ensure proper connection to both Mastodon and Memos APIs.')
@click.option('--config-path', default='config.yaml', help='Path to the configuration file.')
def troubleshoot(config_path):
    """CLI tool to ensure proper connection to both Mastodon and Memos APIs."""

    # Validate and read the configuration file
    _validate_and_read_config(config_path)

    # Initialize the Mastodon and Memos clients and report success
    _initialize_clients(report_success=True)

    # Check if the Mastodon username can be resolved to a user ID
    user_id = mastodon_client.get_user_id_from_username(config['mastodon']['username'])
    if user_id:
        click.echo(f'Successfully resolved Mastodon username to user ID: {user_id}')
    else:
        click.echo('Failed to resolve Mastodon username to user ID.')
        exit(1)

    # At this point, we can assume that the connection to both APIs is successful

    return True

def _validate_and_read_config(config_path):
    """
    Validate and read the configuration file.
    :param config_path: Path to the configuration file.
    """
    global config

    if not os.path.exists(config_path):
        click.echo(f'Configuration file not found at {config_path}. Please ensure the file exists.')
        exit(1)

    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)

    expected_keys = {
        'mastodon': ['api_url', 'client_id', 'client_secret', 'access_token', 'username'],
        'memos': ['api_url', 'access_token']
    }

    for section, keys in expected_keys.items():
        if section not in config:
            click.echo(f'Missing section "{section}" in configuration file.')
            exit(1)
        for key in keys:
            if key not in config[section]:
                click.echo(f'Missing key "{key}" in section "{section}" of configuration file.')
                exit(1)

def _initialize_clients(report_success):
    """Initialize Mastodon and Memos clients."""
    global mastodon_client, memos_client

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
            click.echo('Successfully connected to Mastodon API.')
    else:
        click.echo('Failed to connect to Mastodon API.')
        exit(1)

    # Test Memos connection
    memos_status = memos_client.test_connection()
    if memos_status:
        if report_success:
            click.echo('Successfully connected to Memos API.')
    else:
        click.echo('Failed to connect to Memos API.')
        exit(1)

cli.add_command(mastodon2memos)
cli.add_command(troubleshoot)

if __name__ == '__main__':
    cli()
