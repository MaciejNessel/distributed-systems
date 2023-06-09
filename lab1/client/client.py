import signal
import sys
import uuid
import logging

from client.client_multicast import ClientMulticast
from client.client_udp import ClientUdp
from client.client_tcp import ClientTcp
from common.client_send_mode import ClientSendMode
from common.message import Message, MessageTypes
from utils.ascii_loader import AsciiArt
from utils.command import get_command_attr


class Client:
    def __init__(self, nick, port, config):
        self.config = config

        self.nick = nick
        self.port = port
        self.id = uuid.uuid4()
        self.mode = self.config.client_default_mode

        server_address = (self.config.server_ip_address, self.config.server_port)
        client_address = (self.config.client_ip_address, self.port)
        self.tcp_client = ClientTcp(client_address, server_address, self.config.max_message_size)
        self.udp_client = ClientUdp(client_address, server_address, self.config.max_message_size)
        self.multicast_client = ClientMulticast(self.config.multicast_group, self.config.multicast_port, self.config.max_message_size)

    def prepare_message(self, message_type: MessageTypes, content=None):
        message = Message(message_type, str(self.id), self.nick, content)
        message_formatted = message.to_json().encode()
        return message_formatted

    def send_message(self, content):
        message = self.prepare_message(MessageTypes.MESSAGE.value, content)
        if len(message) > self.config.max_message_size:
            logging.error(f"Message size limit exceeded. [max: {self.config.max_message_size}] Not sent.")
            return
        if self.mode == ClientSendMode.TCP.value:
            self.tcp_client.send(message)
        elif self.mode == ClientSendMode.UDP.value:
            self.udp_client.send(message)
        elif self.mode == ClientSendMode.MULTICAST.value:
            self.multicast_client.send(message)
        else:
            logging.error(f"Invalid mode '{self.mode}'!")

    def register(self):
        message = self.prepare_message(MessageTypes.REGISTER.value)
        self.tcp_client.send(message)
        self.udp_client.send(message)

    def unregister(self):
        message = self.prepare_message(MessageTypes.UNREGISTER.value)
        self.tcp_client.send(message)
        self.udp_client.send(message)

    def mode_handler(self, command):
        new_mode = get_command_attr(command, "--mode ")
        if not new_mode:
            logging.error("Invalid command. Usage: --mode [mode]")
            return

        valid_modes = [mode.value for mode in ClientSendMode]
        if new_mode in valid_modes:
            self.mode = new_mode
            logging.info(f"Changed mode to '{new_mode}'")
        else:
            logging.error(f"Invalid mode '{new_mode}'. Allowed modes are: {valid_modes}")

    def file_handler(self, command):
        filename = get_command_attr(command, "--file ")
        if not filename:
            logging.error("Invalid command. Usage: --file [filename]")
            return

        return AsciiArt.load(filename)

    def start(self):
        self.tcp_client.start()
        self.udp_client.start()
        self.multicast_client.start()

        self.register()

        signal.signal(signal.SIGINT, self.stop)
        while True:
            command = input(f"[{self.mode}:{self.nick}] ")
            if "--mode" in command:
                self.mode_handler(command)
            elif "--file" in command:
                message = self.file_handler(command)
                if message:
                    self.send_message(message)
                else:
                    logging.error("Error during file loading. Message was not sent.")
            elif len(command):
                self.send_message(command)

    def stop(self, sig, frame):
        self.unregister()
        self.tcp_client.stop()
        self.udp_client.stop()
        self.multicast_client.stop()
        sys.exit(0)
