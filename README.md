# gpt-slack-bot

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
