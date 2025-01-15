import click
from mastodon2memos import _
from mastodon2memos.commands import initialize_clients, validate_and_read_config

@click.command(name='troubleshoot', 
               help=_('Ensure proper connection to both Mastodon and Memos APIs.'))
@click.option('--config-path', default='config.yaml', help=_('Path to the configuration file.'))
def troubleshoot(config_path):
    """CLI tool to ensure proper connection to both Mastodon and Memos APIs."""

    # Validate and read the configuration file
    config = validate_and_read_config(config_path)

    # Initialize the Mastodon and Memos clients and report success
    mastodon_client, memos_client = initialize_clients(config, report_success=True)

    # Check if the Mastodon username can be resolved to a user ID
    user_id = mastodon_client.get_user_id_from_username(config['mastodon']['username'])
    if user_id:
        click.echo(_('Successfully resolved Mastodon username to user ID: {user_id}').format(user_id=user_id))
    else:
        click.echo(_('Failed to resolve Mastodon username to user ID.'))
        exit(1)

    # At this point, we can assume that the connection to both APIs is successful

    return True
