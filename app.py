import asyncio

from slack_bolt.adapter.socket_mode.async_handler import AsyncSocketModeHandler
from slack_bolt.app.async_app import AsyncApp

import simple_qa
from constant import slack_app_token, slack_bot_token
from database import create_session

app = AsyncApp(token=slack_bot_token)

session = create_session()


@app.event("app_mention")
async def handle_mentions(event, say):
    await simple_qa.say_answer(event, say, session)


@app.event("message")
async def handle_message(event, say):
    # handle only for direct messages
    if event.get("channel_type") != "im":
        return

    await simple_qa.say_answer(event, say, session)


async def main():
    handler = AsyncSocketModeHandler(app, slack_app_token)
    await handler.start_async()


if __name__ == "__main__":
    asyncio.run(main())
