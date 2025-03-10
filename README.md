# Mastodon2Memos

A Python script that reads your "public" Mastodon AND/OR Bluesky toots & captures them in a Memos instance as "public" memos.

Memos is a privacy-first, lightweight note-taking solution that allows you to effortlessly capture and share your ideas. See [Memos](https://www.usememos.com/) for more.

**Important note:** Mastodon2Memos relies on the Memos API, which is currently in beta. 
Thus, as the API may change, this script may stop working at any time.
The latest version of Memos that this script has been tested against is [v0.24.0](https://github.com/usememos/memos/releases/tag/v0.24.0).

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/dandelionmood/mastodon2memos.git
    cd mastodon2memos
    ```

2. Create a virtual environment:
    ```sh
    python3 -m venv venv
    source venv/bin/activate
    ```

3. Install the dependencies:
    ```sh
    pip install -r requirements.txt
    ```

## Configuration 

Copy the example configuration file to the expected location:
```sh
cp config.yaml.dist config.yaml
```
**Notes:** 
- `config.yaml` is the default configuration file name, and it is expected to be in the root directory of the project by default. 
- Both commands can be run using the optional `--config-path` option which allows you to specify an alternative path to the configuration file. 

### Mastodon settings 

Update the `mastodon` section in the `config.yaml` file with information from your Mastodon instance.

You need to set the `enabled` key to "true" to enable the Mastodon integration. Leave it set to "false" if you don't want to use Mastodon.

Set the `api_url` to the instance URL (e.g., "https://mastodon.social").

Create a Mastodon application in the Development section of your instance account to obtain the necessary values for the `client_id`, `client_secret`, and `access_token` keys. You can opt to only grant "read" access, which should be sufficient.

Set the `username` configuration key to the username on the instance from which you want to scrape content. Note: The script expects this account to be on the same instance server.

### Bluesky settings

Update the `bluesky` section in the `config.yaml` file with information from your Bluesky instance.

You need to set the `enabled` key to "true" to enable the Bluesky integration. Leave it set to "false" if you don't want to use Bluesky.

Set the `api_url` to the instance URL (e.g., "https://bsky.social").
Note: this URL is currently the only supported instance, and the underlying code expects it to be set to this value anyway.

Create a Bluesky application in the Development section of your instance account to obtain the necessary values for the `password` key.

The `handle` key is the username of the account you want to use to publish memos. It is expected to be in the format `handle.bsky.social`.

### Memos settings

Update the `memos` section in the `config.yaml` file with information from your Memos instance.

Set the `api_url` to the root URL of your Memos instance (e.g., "https://mymemos.test.org").

Generate an access token from the settings of the target account. Go to the "My Account" section, add a new access token, and copy its value to the `access_token` key in the configuration file. It is recommended to set the token to never expire to prevent the script from breaking in the future.

## Usage

Available commands are:
- `troubleshoot`: ensure that the connection to both the Mastodon and Memos instances can be properly established.
- `mastodon2memos`: import Mastodon posts as Memos.
- `bluesky2memos`: import Bluesky posts as Memos.

### troubleshoot - Is everything alright?

Ensure that the connection to both the Mastodon and Memos instances can be properly established using the `troubleshoot` command.

To run the command, execute the following:

```sh
python cli.py troubleshoot
```

This will check the status of the connections and let you know if something is not set up properly.

The troubleshoot command performs the following checks and provide explicit feedback:
- Is the configuration file in the expected location?
- Are all the expected configuration keys present in the configuration file?
- Is either Mastodon or Bluesky enabled in the configuration?
- Can the specified Mastodon `username` be resolved to a user_id?
- Can the specified Bluesky `handle` be resolved to a user_id?

If the `troubleshoot` command is successful, you can move on to using the other commands.

### mastodon2memos - Mastodon2Memos command

**Important notes:**
- The script currently takes the last 30 toots and tries to import them. Anything older than that will be ignored.
- Memos converted from toots keep a reference to the original toot URL, which is used to ensure that no toot is added twice. No update is performed, so if you really want a toot to be updated, delete the related memo and run the script again.

#### Interactive mode

To test the waters, you might want to run the script in `--interactive` mode first.

This will ask before attempting to add new toots as memos and let you review changes at each step.

Note: existing memos for the same toot will be skipped anyway.

This can be called using the `--interactive` option:

```sh
python cli.py mastodon2memos --interactive
```

When everything is OK, you can finally start the script in non-interactive mode.

This can be achieved using the command:

```sh
python cli.py mastodon2memos
```

### bluesky2memos - Bluesky2Memos command

The `bluesky2memos` command is similar to the `mastodon2memos` command, but it only processes posts from the specified Bluesky handle.

To run the command, execute the following:

```sh
python cli.py bluesky2memos
```

## Production mode

You can set up the desired script in your crontab to run it regularly. Open your crontab file with the following command:

```sh
crontab -e
```

Add the following line to schedule its execution:

```sh
*/15 * * * * cd /home/user/src/mastodon2memos && . venv/bin/activate && python cli.py mastodon2memos >> /tmp/mastodon2memos.log 2>&1
```

This will run the `mastodon2memos` script every 15 minutes and log execution details to the `/tmp/mastodon2memos.log` file with a standard out redirection. Feel free to remove the `>>` redirection if you don't need full execution logs.

**Note: the path to the script (here `/home/user/src/mastodon2memos`) needs to be updated with the actual location of the project source code repository.**

### Handling imports from multiple accounts

If you want to use the script to publish memos from **multiple** mastodon/bluesky accounts, you can use the `--config-path` option to specify a different configuration file for each account. 

## Development

Install the testing dependencies:

```sh
pip install -r requirements-tests.txt
```

Set up a distinct configuration dedicated to the unit tests:

```sh
cp config.yaml.dist config_test.yaml
```

`config_test.yaml` is the default configuration file name, and it is expected to be in the root directory of the project by default.

**Note: Unit tests for this project do not use mock objects.** Instead, it is expected that you set up test instances or accounts on both Mastodon and Memos. This ensures that the tests interact with real data and APIs, providing more accurate and reliable results.

The test suite can then be run with `unittest`:

```sh
python -m unittest discover
```

## Contributing

Contributions are welcome! If you have any ideas, suggestions, or bug reports, please open an issue or submit a pull request.

1. Fork the repository.
2. Create a new branch for your feature or bugfix:
    ```sh
    git checkout -b my-feature-branch
    ```
3. Make your changes.
4. Commit your changes:
    ```sh
    git commit -m "Description of my changes"
    ```
5. Push to the branch:
    ```sh
    git push origin my-feature-branch
    ```
6. Open a pull request on GitHub.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.