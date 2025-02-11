import click
from mastodon2memos import _
from mastodon2memos.commands import initialize_bluesky_client, is_bluesky_enabled, validate_and_read_config, initialize_memos_client
from mastodon2memos.converters.bluesky2memos_converter import Bluesky2Memos_Converter
from tqdm import tqdm

@click.command(name='bluesky2memos', 
               help=_('Publish Bluesky posts as Memos.'))
@click.option('--interactive', is_flag=True, help=_('Ask before creating a new memo from a post.'))
@click.option('--config-path', default='config.yaml', help=_('Path to the configuration file.'))
def bluesky2memos(interactive, config_path):
    """CLI tool to publish Bluesky posts as Memos."""

    try:
        # Validate and read the configuration file
        config = validate_and_read_config(config_path)
    except Exception as e:
        raise click.ClickException(str(e))

    # Stop execution if bluesky is not enabled
    if is_bluesky_enabled(config) is False:
        raise click.ClickException(_('Bluesky is not enabled in the configuration file.'))
    
    # Initialize our Bluesky and Memos clients
    bluesky_client = initialize_bluesky_client(config)
    memos_client = initialize_memos_client(config)
    bluesky2memos_converter = Bluesky2Memos_Converter(memos_client, bluesky_client)

    # Get the user DID from the Bluesky handle
    user_did = bluesky_client.get_user_did_from_handle(config['bluesky']['handle'])
    # Get the latest posts
    feed = bluesky_client.get_latest_posts(user_did, limit=30)  # Load 30 posts

    # Attempt to publish each new post as a memo
    posts_to_process = tqdm(feed, desc=_('Processing posts'), unit=_('post'), ncols=80, colour="blue", leave=False) \
        if not interactive \
        else feed
    
    for item in posts_to_process:
        
        post = item.post
        post_url = bluesky_client.get_post_url(post)
        if interactive:
            click.echo(click.style(_('Processing post: {url}').format(url=post_url), fg='blue'))
            click.echo(click.style(_('Content:\n{content}').format(content=post.record.text), fg='blue')) 

        # Check if the post is already saved as a memo
        if memos_client.find_by_bluesky_post_url(post_url):
            if interactive:
                click.echo(click.style('✘ ' + _('Post already saved in memos, skipping.'), fg='yellow'))
            continue

        if interactive:
            if not click.confirm(_('Do you want to attempt publishing this post as a memo?')):
                click.echo(click.style('✘ ' + _('Skipping post.'), fg='yellow'))
                continue

        try:
            memo = bluesky2memos_converter.publish_post_as_memo(post)
            if interactive:
                click.echo(click.style('✔ ' + _('New post added to memos.'), fg='green'))
                click.echo(memos_client.get_memo_url(memo["name"]))
        except RuntimeError as e:
            if interactive:
                click.echo(click.style('✘ ' + _('No memo added, an unexpected error occurred.'), fg='red'))
        
        if interactive:
            click.echo('---')
        
    click.echo(click.style(_('Finished processing posts.'), fg='green'))

    return True