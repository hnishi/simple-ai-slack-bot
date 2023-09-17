from dataclasses import dataclass
from typing import Literal

MessageRole = Literal["system", "user", "assistant", "function"]


@dataclass
class Message:
    channel_id: str
    thread_ts: str
    role: MessageRole
    sender: str
    receiver: str
    content: str
    timestamp: str
