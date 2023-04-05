import os
import re
import aiohttp

from slack_sdk import WebClient

from slack_bolt.app.async_app import AsyncApp
from slack_bolt.adapter.socket_mode.async_handler import AsyncSocketModeHandler
import openai

from database import create_session, Message

openai.api_key = os.getenv("OPENAI_API_KEY")
slack_bot_token = os.getenv("SLACK_BOT_TOKEN")
slack_app_token = os.getenv("SLACK_APP_TOKEN")

bot_id = WebClient(token=slack_bot_token).auth_test()["user_id"]

app = AsyncApp(token=slack_bot_token)

session = create_session()

MODEL_NAME = "gpt-3.5-turbo"

SYSTEM_PROMPT = """
あなたは有能な Slack Bot です。
以後、スレッドのメッセージが全て渡されます。
最後のメッセージに対して応答してください。
"""


async def generate_answer(messages):
    input = [{"role": "system", "content": SYSTEM_PROMPT}]
    for message in messages:
        input.append({"role": message.role, "content": message.content})

    async with aiohttp.ClientSession() as session:
        response = await session.post(
            "https://api.openai.com/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {openai.api_key}",
                "Content-Type": "application/json",
            },
            json={
                "model": MODEL_NAME,
                "messages": input,
            },
        )
        response_data = await response.json()
        return response_data["choices"][0]["message"]["content"]


@app.event("app_mention")
async def handle_mentions(event, say):
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

    answer = await generate_answer(messages)
    await say(text=answer, thread_ts=thread_ts)

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


async def main():
    handler = AsyncSocketModeHandler(app, slack_app_token)
    await handler.start_async()


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
