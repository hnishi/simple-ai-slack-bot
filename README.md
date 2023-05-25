# gpt-slack-bot

## Slack

1. Create an Slack app

    - See [the document](https://slack.dev/bolt-python/tutorial/getting-started).

1. Socket Mode

    - On

1. Bot Token Scopes

    - app_mentions:read
    - chat:write

1. App Token Scopes

    - connections:write

1. Event Subscriptions (Subscribe to bot events)

    - app_mentions:read

## Usage

### Prerequisites

1. [Recommended] Create a Python virtual environment

    Using a Python virtual environment is recommended for isolating dependencies.

    ```shell
    python -m venv .venv
    source .venv/bin/activate
    ```

1. Install the required packages

    ```shell
    pip install -r requirements.txt
    ```

### Configuration

1. Set the necessary environment variables

    ```shell
    export SLACK_BOT_TOKEN=xoxb-xxx
    export SLACK_APP_TOKEN=xapp-xxx
    export OPENAI_API_KEY=xxx
    ```

### Running the application

1. Run the application

    ```shell
    python app.py
    ```

## References

- [Slack | Bolt for Python](https://slack.dev/bolt-python/concepts)
- [GitHub - openai/openai-python: The OpenAI Python library provides convenient access to the OpenAI API from applications written in the Python language.](https://github.com/openai/openai-python)
