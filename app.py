from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

import simple_qa
from constant import slack_app_token, slack_bot_token
from database import create_session

app = App(token=slack_bot_token)

session = create_session()


@app.event("app_mention")
def handle_mentions(event, say):
    simple_qa.say_answer(event, say, session)


@app.event("message")
def handle_message(event, say):
    # handle only for direct messages
    if event.get("channel_type") != "im":
        return

    simple_qa.say_answer(event, say, session)


if __name__ == "__main__":
    SocketModeHandler(app, slack_app_token).start()
