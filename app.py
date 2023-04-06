import os
import re

from slack_sdk import WebClient
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
import openai
import tiktoken

from database import create_session, Message

openai.api_key = os.getenv("OPENAI_API_KEY")
slack_bot_token = os.getenv("SLACK_BOT_TOKEN")
slack_app_token = os.getenv("SLACK_APP_TOKEN")

bot_id = WebClient(token=slack_bot_token).auth_test()["user_id"]

app = App(token=slack_bot_token)

session = create_session()

MODEL_NAME = "gpt-3.5-turbo"
MODEL_MAX_TOKEN_LENGTH = 4097

SYSTEM_PROMPT = f"""
あなたは OpenAI API の {MODEL_NAME} モデルを利用した有能な Slack Bot です。
あなたの Bot ID は {bot_id} です。
"""


def generate_answer(messages):
    enc = tiktoken.encoding_for_model(MODEL_NAME)
    input = [{"role": "system", "content": SYSTEM_PROMPT}]
    total_token_length = len(enc.encode(SYSTEM_PROMPT))
    for message in reversed(messages):
        token_length = len(enc.encode(message.content))
        # なぜかOpenAIサーバー側のトークンカウントと微妙に一致しないため、係数 0.9 を使う
        if total_token_length + token_length > MODEL_MAX_TOKEN_LENGTH * 0.9:
            break
        input.insert(1, {"role": message.role, "content": message.content})
        total_token_length += token_length
    try:
        completion = openai.ChatCompletion.create(model=MODEL_NAME, messages=input)
        return completion.choices[0].message["content"]
    except openai.error.InvalidRequestError as e:
        return str(e)


@app.event("app_mention")
def handle_mentions(event, say):
    channel_id = event["channel"]
    thread_ts = event.get("thread_ts", event["ts"])
    user_id = event["user"]
    content = event["text"]
    mentioned_users = re.findall(r"<@([A-Z0-9]+)>", content)

    user_message = Message(
        channel_id=channel_id,
        thread_ts=thread_ts,
        role="user",
        sender=user_id,
        # TODO: 複数ユーザーにメンションされた場合の処理は未検討
        receiver=mentioned_users[0],
        content=content,
    )
    session.add(user_message)
    session.commit()

    messages = (
        session.query(Message)
        .filter(Message.thread_ts == thread_ts)
        .order_by(Message.id)
        .all()
    )

    answer = generate_answer(messages)
    say(text=answer, thread_ts=thread_ts)

    assistant_message = Message(
        channel_id=channel_id,
        thread_ts=thread_ts,
        role="assistant",
        sender=bot_id,
        receiver=user_id,
        content=answer,
    )
    session.add(assistant_message)
    session.commit()


if __name__ == "__main__":
    SocketModeHandler(app, slack_app_token).start()
