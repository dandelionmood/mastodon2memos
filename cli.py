import click
import yaml

from mastodon2memos.mastodon import MastodonClient
from mastodon2memos.memos import MemosClient

@click.group()
def cli():
    """CLI tool for Mastodon to Memos operations."""
    pass

@click.command(name='mastodon2memos', 
               help='Publish Mastodon toots as Memos.')
@click.option('--interactive', is_flag=True, help='Ask before creating a new memo from a toot.')
def mastodon2memos(interactive):
    """CLI tool to publish Mastodon toots as Memos."""

    # Initialize the Mastodon and Memos clients
    _initialize_clients()

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
def troubleshoot():
    """CLI tool to ensure proper connection to both Mastodon and Memos APIs."""

    # Initialize the Mastodon and Memos clients
    _initialize_clients()

    # Test Mastodon connection
    mastodon_status = mastodon_client.test_connection()
    if mastodon_status:
        click.echo('Successfully connected to Mastodon API.')
    else:
        click.echo('Failed to connect to Mastodon API.')
        return False

    # Test Memos connection
    memos_status = memos_client.test_connection()
    if memos_status:
        click.echo('Successfully connected to Memos API.')
    else:
        click.echo('Failed to connect to Memos API.')
        return False

    return True

def _initialize_clients(config_path='config.yaml'):
    """Initialize Mastodon and Memos clients and set them as global variables."""
    global mastodon_client, memos_client, config
    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)
    
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

cli.add_command(mastodon2memos)
cli.add_command(troubleshoot)

if __name__ == '__main__':
    cli()
