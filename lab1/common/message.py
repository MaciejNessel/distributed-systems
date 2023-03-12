import json
from dataclasses import dataclass, asdict
from enum import Enum


class MessageTypes(Enum):
    MESSAGE = "message"
    REGISTER = "register"
    UNREGISTER = "unregister"


@dataclass
class Message:
    type: MessageTypes
    id: str = None
    nick: str = None
    content: str = None

    def to_dict(self):
        return asdict(self)

    def to_json(self):
        return json.dumps(self.to_dict())
