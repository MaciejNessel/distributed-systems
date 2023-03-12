import json
from dataclasses import dataclass, asdict


@dataclass
class Message:
    id: str
    nick: str
    content: str

    def to_dict(self):
        return asdict(self)

    def to_json(self):
        return json.dumps(self.to_dict())
