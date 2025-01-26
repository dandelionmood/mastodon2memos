import click

from mastodon2memos.commands.bluesky2memos import bluesky2memos
from mastodon2memos.commands.mastodon2memos import mastodon2memos
from mastodon2memos.commands.troubleshoot import troubleshoot

@click.group()
def cli():
    """CLI tool for Mastodon to Memos operations."""
    pass

cli.add_command(mastodon2memos)
cli.add_command(bluesky2memos)
cli.add_command(troubleshoot)

if __name__ == '__main__':
    cli()
