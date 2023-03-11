import uuid
import logging
from dataclasses import asdict
from enum import Enum

from client_tcp import ClientTcp
from common.message import Message
from utils.config import Config


class Mode(Enum):
    TCP = "T"
    UDP = "U"
    MULTICAST = "M"


class Client:
    def __init__(self, nick):
        self.nick = nick
        self.id = uuid.uuid4()
        self.config = Config()
        self.mode = Mode.TCP.value

        self.tcp_client = ClientTcp(self.config.server_url, self.config.server_port)
        self.start()


    def change_mode(self, new_mode):
        valid_modes = [mode.value for mode in Mode]
        if new_mode in valid_modes:
            self.mode = new_mode
            logging.info(f"Changed mode to '{new_mode}'")
        else:
            logging.error(f"Invalid mode '{new_mode}'. Allowed modes are: {valid_modes}")

    def send_message(self, content):
        message = Message(str(self.id), self.nick, content)
        to_send = str(asdict(message))
        print(to_send)
        match self.mode:
            case Mode.TCP.value:
                result = self.tcp_client.send(to_send)
                print(result)
            case _: logging.error(f"Invalid mode '{self.mode}'!")


    def mode_handler(self, command):
        mode_arg = command.split("--mode ")
        if len(mode_arg) == 2:
            new_mode = mode_arg[1].strip()
            self.change_mode(new_mode)
        else:
            print("Invalid command. Usage: --mode [mode]")

    def start(self):
        while True:
            command = input(f"[{self.mode}:{self.nick}] ")
            if "--mode" in command:
                self.mode_handler(command)
            elif "--close" in command:
                self.close()
            elif len(command):
                self.send_message(command)




    def close(self):
        self.tcp_client.close()

