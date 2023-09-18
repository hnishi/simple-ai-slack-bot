# simple-ai-slack-bot

Simple Slack bot powered by OpenAI Chat API.

You can talk to the chat bot using OpenAI Chat API via Slack.

## Usage in Slack

### Public and private channels in which the bot is added

You have to mention the bot to talk to it.

![screenshot](attachments/2023-09-17-19-18-49.png)

### Direct messages to the bot

You can talk to the bot without mentioning it.

![screenshot](attachments/2023-09-17-19-18-15.png)

## Slack App Configuration

1. Create an Slack app

    - See [the document](https://slack.dev/bolt-python/tutorial/getting-started).

1. Socket Mode

    - On

1. Bot Token Scopes

    - app_mentions:read
    - chat:write
    - im:history
    - im:read
    - im:write

1. App Token Scopes

    - connections:write

1. Event Subscriptions (Subscribe to bot events)

    - app_mentions:read
    - message.im

1. Messages Tab

    - App Home --> Show Tabs --> Messages Tab
    - Check `Allow users to send Slash commands and messages from the messages tab`

## Prerequisites

1. Poetry

    Poetry is used to manage the dependencies.

    See https://python-poetry.org/docs/#installation

1. Install the required packages

    ```shell
    poetry install --no-root
    ```

## App Configuration

1. Create the `.env` file

    ```shell
    cp .env.sample .env
    ```

1. Set the necessary environment variables in the `.env` file

    ```shell
    SLACK_BOT_TOKEN=xoxb-xxx
    SLACK_APP_TOKEN=xapp-xxx
    OPENAI_API_KEY=sk-xxx
    OPENAI_ORGANIZATION=org-xxx  # this parameter is optional
    MODEL_NAME=gpt-3.5-turbo
    ```

    For model name, see https://platform.openai.com/docs/models/overview

## Running the application

1. Run the application

    ```shell
    poetry run python app.py
    ```

## Docker

### Build

```shell
docker build -t simple-ai-slack-bot .
```

### Run

```shell
docker run -it simple-ai-slack-bot
```

### docker compose

```shell
docker-compose up
```

## References

- [Slack | Bolt for Python](https://slack.dev/bolt-python/concepts)
- [GitHub - openai/openai-python: The OpenAI Python library provides convenient access to the OpenAI API from applications written in the Python language.](https://github.com/openai/openai-python)
- [OpenAI API Documentation](https://platform.openai.com/docs/introduction)
