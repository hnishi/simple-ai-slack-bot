# Ref: https://github.com/Significant-Gravitas/Auto-GPT/blob/84890523586508a89debab836dcb71bdb48983bd/autogpts/autogpt/autogpt/llm/utils/token_counter.py

"""Functions for counting the number of tokens in a message or string."""
from __future__ import annotations

import logging
from typing import List, Protocol, Union

import tiktoken

import database
import models.message

logger = logging.getLogger(__name__)


class HasRoleAndContent(Protocol):
    role: str
    content: str


def count_message_tokens(
    messages: Union[HasRoleAndContent, List[HasRoleAndContent]],
    model: str = "gpt-3.5-turbo",
) -> int:
    """
    Returns the number of tokens used by a list of messages.

    Args:
        messages (list): A list of messages, each of which is a dictionary
            containing the role and content of the message.
        model (str): The name of the model to use for tokenization.
            Defaults to "gpt-3.5-turbo-0301".

    Returns:
        int: The number of tokens used by the list of messages.
    """
    if isinstance(messages, Union[database.Message, models.message.Message]):
        messages = [messages]

    if model.startswith("gpt-3.5-turbo"):
        tokens_per_message = (
            4  # every message follows <|start|>{role/name}\n{content}<|end|>\n
        )
        # tokens_per_name = -1  # if there's a name, the role is omitted
        encoding_model = "gpt-3.5-turbo"
    elif model.startswith("gpt-4"):
        tokens_per_message = 3
        # tokens_per_name = 1
        encoding_model = "gpt-4"
    else:
        supported_models = ["gpt-3.5-turbo", "gpt-4"]
        raise NotImplementedError(
            f"count_message_tokens() is not implemented for model {model}.\n"
            f"Supported models are: {', '.join(supported_models)}\n"
            " See https://github.com/openai/openai-python/blob/main/chatml.md for"
            " information on how messages are converted to tokens."
        )
    try:
        encoding = tiktoken.encoding_for_model(encoding_model)
    except KeyError:
        logger.warn("Warning: model not found. Using cl100k_base encoding.")
        encoding = tiktoken.get_encoding("cl100k_base")

    num_tokens = 0
    for message in messages:
        num_tokens += tokens_per_message
        num_tokens += len(encoding.encode(message.role))
        num_tokens += len(encoding.encode(message.content))
    num_tokens += 3  # every reply is primed with <|start|>assistant<|message|>
    return num_tokens


def count_string_tokens(string: str, model_name: str) -> int:
    """
    Returns the number of tokens in a text string.

    Args:
        string (str): The text string.
        model_name (str): The name of the encoding to use. (e.g., "gpt-3.5-turbo")

    Returns:
        int: The number of tokens in the text string.
    """
    encoding = tiktoken.encoding_for_model(model_name)
    return len(encoding.encode(string))
