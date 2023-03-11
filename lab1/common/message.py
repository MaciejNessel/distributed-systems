from dataclasses import dataclass, asdict


@dataclass
class Message:
    id: str
    nick: str
    content: str
