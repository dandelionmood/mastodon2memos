import click
import traceback
from mastodon2memos import _
from mastodon2memos.commands import is_bluesky_enabled, is_mastodon_enabled, validate_and_read_config, initialize_mastodon_client, initialize_memos_client, initialize_bluesky_client

@click.command(name='troubleshoot', 
               help=_('Ensure proper connection to Mastodon, Bluesky, and Memos APIs.'))
@click.option('--config-path', default='config.yaml', help=_('Path to the configuration file.'))
@click.option('--verbose', is_flag=True, help=_('Display full stack trace on error.'))
def troubleshoot(config_path, verbose):
    """CLI tool to ensure proper connection to Mastodon, Bluesky, and Memos APIs."""

    click.echo(_('Reading configuration from: {config_path}').format(config_path=config_path))
    
    try:
        # Validate and read the configuration file
        config = validate_and_read_config(config_path)
    except Exception as e:
        raise click.ClickException(str(e))

    mastodon_enabled = is_mastodon_enabled(config)
    bluesky_enabled = is_bluesky_enabled(config)

    if not mastodon_enabled and not bluesky_enabled:
        raise click.ClickException(_('Neither Mastodon nor Bluesky connections are enabled in the configuration.'))

    if mastodon_enabled:
        try:
            # Initialize the Mastodon client and report success
            mastodon_client = initialize_mastodon_client(config)

            # Performing a couple calls to test the connection
            user_id = mastodon_client.get_user_id_from_username(config['mastodon']['username'])
            mastodon_client.get_latest_public_toots(user_id)

            # At this stage, we can assume that the connection is successful
            click.echo('✔ ' + _('Successfully connected to Mastodon API.'))
            if user_id:
                click.echo(_('Successfully resolved Mastodon username to user ID: {user_id}').format(user_id=user_id))
            else:
                click.echo(_('Failed to resolve Mastodon username to user ID.'))
                exit(1)
        except Exception as e:
            click.echo('\n✘ ' + _('Failed to connect to Mastodon API: {error}').format(error=str(e)))
            if verbose:
                click.echo('\n' + traceback.format_exc())
            exit(1)

    if bluesky_enabled:
        try:
            # Initialize the Bluesky client and report success
            bluesky_client = initialize_bluesky_client(config)

            # Performing a couple calls to test the connection
            user_id = bluesky_client.get_user_did_from_handle(config['bluesky']['handle'])
            bluesky_client.get_latest_posts(user_id)

            # At this stage, we can assume that the connection is successful
            click.echo('\n✔ ' + _('Successfully connected to Bluesky API.'))
            if user_id:
                click.echo(_('Successfully resolved Bluesky username to user ID: {user_id}').format(user_id=user_id))
            else:
                click.echo(_('Failed to resolve Bluesky username to user ID.'))
                exit(1)
        except Exception as e:
            click.echo('\n✘ ' + _('Failed to connect to Bluesky API: {error}').format(error=str(e)))
            if verbose:
                click.echo('\n' + traceback.format_exc())
            exit(1)

    try:
        # Initialize the Memos client and report success
        memos = initialize_memos_client(config)
        # We test by looking for a memo with a toot URL
        # It does not matter that it will return None, as long as it does not raise an exception
        memos.find_by_toot_url("https://mastodon.social/users/loremipsum/statuses/100")
    
        # At this stage, we can assume that the connection is successful
        click.echo('\n✔ ' + _('Successfully connected to Memos API.'))
    except Exception as e:
        click.echo('\n✘ ' + _('Failed to connect to Memos API: {error}').format(error=str(e)))
        if verbose:
            click.echo('\n' + traceback.format_exc())
        exit(1)

    # At this point, we can assume that the connection to the configured APIs is successful

    return True
