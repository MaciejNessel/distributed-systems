import threading
import uuid
import logging
from enum import Enum

from client_udp import ClientUdp
from client_tcp import ClientTcp
from common.message import Message
from utils.ascii_loader import AsciiArt
from utils.config import Config


class Mode(Enum):
    TCP = "T"
    UDP = "U"
    MULTICAST = "M"


class Client:
    def __init__(self, nick, port):
        self.nick = nick
        self.port = port
        self.id = uuid.uuid4()
        self.config = Config()
        self.mode = Mode.TCP.value

        self.tcp_client = ClientTcp(self.config.server_url, self.config.server_port)
        self.udp_client = ClientUdp(
            self.port, self.config.server_url, self.config.server_port
        )
        self.is_running = True
        self.start()

    def prepare_message(self, content):
        message = Message(str(self.id), self.nick, content)
        message_formatted = message.to_json()
        return message_formatted

    def send_message(self, content):
        message = self.prepare_message(content)
        if len(message) > self.config.max_message_size:
            logging.error(
                f"Message size limit exceeded. [{len(message)} / max: {self.config.max_message_size}]  Not sent."
            )
            return
        match self.mode:
            case Mode.TCP.value:
                self.tcp_client.send(message)
            case Mode.UDP.value:
                self.udp_client.send(message)
            case _:
                logging.error(f"Invalid mode '{self.mode}'!")

    def mode_handler(self, command):
        mode_arg = command.split("--mode ")
        if len(mode_arg) == 2:
            new_mode = mode_arg[1].strip()
        else:
            print("Invalid command. Usage: --mode [mode]")
            return

        valid_modes = [mode.value for mode in Mode]
        if new_mode in valid_modes:
            self.mode = new_mode
            logging.info(f"Changed mode to '{new_mode}'")
        else:
            logging.error(
                f"Invalid mode '{new_mode}'. Allowed modes are: {valid_modes}"
            )

    def file_handler(self, command):
        file_arg = command.split("--file ")
        if len(file_arg) == 2:
            filename = file_arg[1].strip()
        else:
            print("Invalid command. Usage: --file [filename]")
            return None
        return AsciiArt.load(filename)

    def close_handler(self):
        self.is_running = False
        self.tcp_client.close()
        self.udp_client.close()

    def start(self):
        threading.Thread(target=self.tcp_client.listen, args=()).start()
        threading.Thread(target=self.udp_client.listen, args=()).start()

        while self.is_running:
            command = input(f"[{self.mode}:{self.nick}] ")
            if "--mode" in command:
                self.mode_handler(command)
            elif "--close" in command:
                self.close_handler()
                break
            elif "--file" in command:
                message = self.file_handler(command)
                if message:
                    self.send_message(message)
                else:
                    logging.error("Error during file loading. Message was not sent.")
            elif len(command):
                self.send_message(command)
