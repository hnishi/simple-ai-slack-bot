import os

import openai
from slack_sdk import WebClient

# MODEL_NAME = "gpt-3.5-turbo"
# MODEL_MAX_TOKEN_LENGTH = 4097
MODEL_NAME = "gpt-4"
MODEL_MAX_TOKEN_LENGTH = 8192

SYSTEM_PROMPT = f"""
あなたは OpenAI API の {MODEL_NAME} モデルを利用した Slack Bot です。
"""

openai.api_key = os.getenv("OPENAI_API_KEY")
slack_bot_token = os.getenv("SLACK_BOT_TOKEN")
slack_app_token = os.getenv("SLACK_APP_TOKEN")

bot_id = WebClient(token=slack_bot_token).auth_test()["user_id"]
