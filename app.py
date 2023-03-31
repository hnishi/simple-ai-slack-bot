import os
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")
slack_bot_token = os.getenv("SLACK_BOT_TOKEN")

app = App(token=slack_bot_token)


def generate_answer(content):
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", messages=[{"role": "user", "content": content}]
    )
    return completion.choices[0].message["content"]


@app.event("app_mention")
def handle_mentions(event, say):
    thread_ts = event["ts"]
    answer = generate_answer(event["text"])
    say(text=answer, thread_ts=thread_ts)


if __name__ == "__main__":
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()
