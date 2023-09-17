import re
from typing import List, Optional, Union

import openai
import tiktoken

import database
import models.message
from configuration import (
    IS_MESSAGE_SAVE_ENABLED,
    MODEL_MAX_TOKEN_LENGTH,
    MODEL_NAME,
    SYSTEM_PROMPT,
    bot_id,
    slack_client,
)


def get_thread_messages(
    channel_id: str, thread_ts: str
) -> Optional[List[models.message.Message]]:
    # https://api.slack.com/methods/conversations.replies
    response = slack_client.conversations_replies(channel=channel_id, ts=thread_ts)

    if not response["ok"]:
        print("Error retrieving messages:", response["error"])
        return

    messages = response["messages"]

    outputs = []
    for message in messages:
        if message.get("type") != "message":
            continue

        mentioned_users = re.findall(r"<@([A-Z0-9]+)>", message["text"])

        role = "user" if message["user"] != bot_id else "assistant"

        output = models.message.Message(
            channel_id=channel_id,
            thread_ts=thread_ts,
            role=role,
            sender=message["user"],
            receiver=mentioned_users[0] if len(mentioned_users) > 0 else None,
            content=message["text"],
            timestamp=message["ts"],
        )
        outputs.append(output)
    return outputs


async def generate_answer(
    messages: List[Union[database.Message, models.message.Message]]
):
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
        return "OpenAI API に対する無効なリクエストです。\nエラー詳細: " + str(e)
    except openai.error.APIError as e:
        return "OpenAI API サーバーが API エラーを返しました。時間を置いて再度お試しください。\nエラー詳細: " + str(e)
    except openai.error.RateLimitError as e:
        return "OpenAI API サーバーがレート制限エラーを返しました。\nエラー詳細: " + str(e)
    except Exception as e:
        return "OpenAI API サーバーがエラーを返しました。\nエラー詳細: " + str(e)


async def say_answer_with_sqlite(event, say, session):
    channel_id = event["channel"]
    thread_ts = event.get("thread_ts", event["ts"])
    user_id = event["user"]
    content = event["text"]
    # mentioned_users = re.findall(r"<@([A-Z0-9]+)>", content)

    user_message = database.Message(
        channel_id=channel_id,
        thread_ts=thread_ts,
        role="user",
        sender=user_id,
        # TODO: 複数ユーザーにメンションされた場合の処理は未検討
        # receiver=mentioned_users[0],
        receiver=bot_id,
        content=content,
    )
    session.add(user_message)
    session.commit()

    messages = (
        session.query(database.Message)
        .filter(database.Message.thread_ts == thread_ts)
        .order_by(database.Message.id)
        .all()
    )

    answer = await generate_answer(messages)
    await say(text=answer, thread_ts=thread_ts)

    assistant_message = database.Message(
        channel_id=channel_id,
        thread_ts=thread_ts,
        role="assistant",
        sender=bot_id,
        receiver=user_id,
        content=answer,
    )
    session.add(assistant_message)
    session.commit()


async def say_answer_without_sqlite(event, say):
    channel_id = event["channel"]
    thread_ts = event.get("thread_ts", event["ts"])
    # mentioned_users = re.findall(r"<@([A-Z0-9]+)>", content)

    messages = get_thread_messages(channel_id, thread_ts)

    answer = await generate_answer(messages)
    await say(text=answer, thread_ts=thread_ts)


async def say_answer(event, say, session):
    if IS_MESSAGE_SAVE_ENABLED:
        await say_answer_with_sqlite(event, say, session)
    else:
        await say_answer_without_sqlite(event, say)
