import click
import yaml

from mastodon2memos.mastodon import MastodonClient
from mastodon2memos.memos import MemosClient

@click.command()
def mastodon2memos():
    """Connect to Mastodon and Memos instances and stream user data."""
    with open('config.yaml', 'r') as file:
        config=yaml.safe_load(file)
    
    mastodon_client = MastodonClient(
        api_base_url=config['api_base_url'],
        client_id=config['client_id'],
        client_secret=config['client_secret'],
        access_token=config['access_token']
    )
    click.echo('Connected to Mastodon instance.')

    memos_client = MemosClient(
        api_base_url=config['memos_api_base_url'],
        access_token=config['memos_access_token']
    )
    click.echo('Connected to Memos instance.')

    mastodon_client.publish_new_toots_on_memos(memos_client)

if __name__ == '__main__':
    mastodon2memos()
