from enum import Enum


class ClientSendMode(Enum):
    TCP = "T"
    UDP = "U"
    MULTICAST = "M"
