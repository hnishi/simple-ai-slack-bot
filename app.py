import os
import re

from slack_sdk import WebClient
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
import openai

from database import create_session, Message

openai.api_key = os.getenv("OPENAI_API_KEY")
slack_bot_token = os.getenv("SLACK_BOT_TOKEN")

bot_id = WebClient(token=slack_bot_token).auth_test()["user_id"]

app = App(token=slack_bot_token)

session = create_session()

SYSTEM_PROMPT = """
あなたは有能な Slack Bot です。
以後、スレッドのメッセージが全て渡されます。
最後のメッセージに対して応答してください。
"""


def generate_answer(messages):
    input = [{"role": "system", "content": SYSTEM_PROMPT}]
    for message in messages:
        input.append({"role": message.role, "content": message.content})
    completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=input)
    return completion.choices[0].message["content"]


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
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()
