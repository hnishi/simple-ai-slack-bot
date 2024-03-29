# Ref: https://github.com/Significant-Gravitas/Auto-GPT/blob/84890523586508a89debab836dcb71bdb48983bd/autogpts/autogpt/tests/unit/test_token_counter.py

import pytest

from models.message import Message
from utils.token_counter import count_message_tokens, count_string_tokens

default_arguments = {
    "channel_id": "C01U6P7LZ8G",
    "thread_ts": "1614553701.000400",
    "sender": "U01U6P7LZ8G",
    "receiver": "U01U6P7LZ8G",
    "timestamp": "1614553701.000400",
}


def test_count_message_tokens():
    messages = [
        Message(role="user", content="Hello", **default_arguments),
        Message(role="assistant", content="Hi there!", **default_arguments),
    ]
    assert count_message_tokens(messages) == 17


def test_count_message_tokens_empty_input():
    """Empty input should return 3 tokens"""
    assert count_message_tokens([]) == 3


def test_count_message_tokens_invalid_model():
    """Invalid model should raise a NotImplementedError"""
    messages = [
        Message(role="user", content="Hello", **default_arguments),
        Message(role="assistant", content="Hi there!", **default_arguments),
    ]
    with pytest.raises(NotImplementedError):
        count_message_tokens(messages, model="invalid_model")


def test_count_message_tokens_gpt_4():
    messages = [
        Message(role="user", content="Hello", **default_arguments),
        Message(role="assistant", content="Hi there!", **default_arguments),
    ]
    assert count_message_tokens(messages, model="gpt-4-0314") == 15


def test_count_string_tokens():
    """Test that the string tokens are counted correctly."""

    string = "Hello, world!"
    assert count_string_tokens(string, model_name="gpt-3.5-turbo-0301") == 4


def test_count_string_tokens_empty_input():
    """Test that the string tokens are counted correctly."""

    assert count_string_tokens("", model_name="gpt-3.5-turbo-0301") == 0


def test_count_string_tokens_gpt_4():
    """Test that the string tokens are counted correctly."""

    string = "Hello, world!"
    assert count_string_tokens(string, model_name="gpt-4-0314") == 4
