import os

import openai
from slack_sdk import WebClient

IS_MESSAGE_SAVE_ENABLED = False  # Save messages to sqlite database

# MODEL_NAME = "gpt-3.5-turbo"
# MODEL_MAX_TOKEN_LENGTH = 4097

# See https://platform.openai.com/docs/models/gpt-4
MODEL_NAME = "gpt-4"
MODEL_MAX_TOKEN_LENGTH = 8192

SYSTEM_PROMPT = f"""
あなたは OpenAI API の {MODEL_NAME} モデルを利用した Slack Bot です。
これから行われる一連の会話は、Slack スレッド上で行われるものです。
過去のスレッドメッセージも含めて、OpenAI API に送信されます。
"""

openai.api_key = os.getenv("OPENAI_API_KEY")
slack_bot_token = os.getenv("SLACK_BOT_TOKEN")
slack_app_token = os.getenv("SLACK_APP_TOKEN")


slack_client = WebClient(token=slack_bot_token)
bot_id = slack_client.auth_test()["user_id"]
