from dataclasses import dataclass, field


@dataclass
class Message:
    channel_id: str
    thread_ts: str
    role: str
    sender: str
    receiver: str
    content: str
    timestamp: str
