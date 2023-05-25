import openai
import tiktoken

from constant import MODEL_MAX_TOKEN_LENGTH, MODEL_NAME, SYSTEM_PROMPT, bot_id
from database import Message


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
        return "OpenAI API に対する無効なリクエストです。\nエラー詳細: " + str(e)
    except openai.error.APIError as e:
        return "OpenAI API サーバーが API エラーを返しました。時間を置いて再度お試しください。\nエラー詳細: " + str(e)
    except openai.error.RateLimitError as e:
        return "OpenAI API サーバーがレート制限エラーを返しました。\nエラー詳細: " + str(e)
    except Exception as e:
        return "OpenAI API サーバーがエラーを返しました。\nエラー詳細: " + str(e)


def say_answer(event, say, session):
    channel_id = event["channel"]
    thread_ts = event.get("thread_ts", event["ts"])
    user_id = event["user"]
    content = event["text"]
    # mentioned_users = re.findall(r"<@([A-Z0-9]+)>", content)

    user_message = Message(
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
