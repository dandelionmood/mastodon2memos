import click
from mastodon2memos import _
from mastodon2memos.commands import initialize_clients, validate_and_read_config

@click.command(name='mastodon2memos', 
               help=_('Publish Mastodon toots as Memos.'))
@click.option('--interactive', is_flag=True, help=_('Ask before creating a new memo from a toot.'))
@click.option('--config-path', default='config.yaml', help=_('Path to the configuration file.'))
def mastodon2memos(interactive, config_path):
    """CLI tool to publish Mastodon toots as Memos."""

    # Validate and read the configuration file
    config = validate_and_read_config(config_path)

    # Initialize the Mastodon and Memos clients
    mastodon_client, memos_client = initialize_clients(config, report_success=False)

    # Get the user ID from the Mastodon username
    user_id = mastodon_client.get_user_id_from_username(config['mastodon']['username'])
    # Get the latest public toots
    new_toots = mastodon_client.get_latest_public_toots(user_id, count=30)  # Load 30 public toots
    # Attempt to publish each new toot as a memo
    for toot in new_toots:
        click.echo('---')
        click.echo(_('Processing toot: {url}').format(url=toot["url"]))

        if interactive:
            if not click.confirm(_('Do you want to attempt publishing this toot as a memo?\n{content}\n{url}?').format(content=toot["content"], url=toot["url"])):
                click.echo(_('Skipping toot.'))
                continue
        memo = memos_client.publish_toot_as_memo(toot)  # Use publish_toot_as_memo method
        if memo:
            click.echo(_('New toot added to memos.'))
        else:
            click.echo(_('No memo added, toot was already saved in memos.'))

    click.echo(_('Finished processing toots.'))
    return True
