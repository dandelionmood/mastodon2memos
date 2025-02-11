import click
from mastodon2memos import _
from mastodon2memos.commands import is_mastodon_enabled, validate_and_read_config, initialize_mastodon_client, initialize_memos_client
from mastodon2memos.converters.mastodon2memos_converter import Mastodon2MemosConverter
from tqdm import tqdm

@click.command(name='mastodon2memos', 
               help=_('Publish Mastodon toots as Memos.'))
@click.option('--interactive', is_flag=True, help=_('Ask before creating a new memo from a toot.'))
@click.option('--config-path', default='config.yaml', help=_('Path to the configuration file.'))
def mastodon2memos(interactive, config_path):
    """CLI tool to publish Mastodon toots as Memos."""

    try:
        # Validate and read the configuration file
        config = validate_and_read_config(config_path)
    except Exception as e:
        raise click.ClickException(str(e))

    # Stop execution if mastodon is not enabled
    if is_mastodon_enabled(config) is False:
        raise click.ClickException(_('Mastodon is not enabled in the configuration file.'))
    
    # Initialize our Mastodon and Memos clients
    mastodon_client = initialize_mastodon_client(config)
    memos_client = initialize_memos_client(config)
    mastodon2memos_converter = Mastodon2MemosConverter(memos_client, mastodon_client)

    # Get the user ID from the Mastodon username
    user_id = mastodon_client.get_user_id_from_username(config['mastodon']['username'])
    # Get the latest public toots
    new_toots = mastodon_client.get_latest_public_toots(user_id, count=30)  # Load 30 public toots

    # Attempt to publish each new toot as a memo
    toots_to_process = tqdm(new_toots, desc=_('Processing toots'), unit=_('toot'), ncols=80, colour="green", leave=False) \
        if not interactive \
        else new_toots
    
    for toot in toots_to_process:

        if interactive:
            click.echo('---')
            click.echo(click.style(_('Processing toot: {url}').format(url=toot["url"]), fg='blue'))
            click.echo(click.style(_('Content:\n{content}').format(content=toot["content"]), fg='blue'))

        # Check if the toot is already saved as a memo
        if memos_client.find_by_toot_url(toot["url"]):
            if interactive:
                click.echo(click.style('✘ ' + _('Toot already saved in memos, skipping.'), fg='yellow'))
            continue

        if interactive:
            if not click.confirm(_('Do you want to attempt publishing this toot as a memo?')):
                click.echo(click.style('✘ ' + _('Skipping toot.'), fg='yellow'))
                continue

        try:
            memo = mastodon2memos_converter.publish_toot_as_memo(toot)
            if interactive:
                click.echo(click.style('✔ ' + _('New toot added to memos.'), fg='green'))
                click.echo(memos_client.get_memo_url(memo["name"]))
        except RuntimeError as e:
            if interactive:
                click.echo(click.style('✘ ' + _('No memo added, an unexpected error occurred.'), fg='red'))

    if interactive:
        click.echo('---')

    click.echo(click.style(_('Finished processing toots.'), fg='green'))
    return True
