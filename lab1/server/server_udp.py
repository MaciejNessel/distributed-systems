import json
import logging
import socket
import threading

from common.message import MessageTypes


class ServerUdp:
    def __init__(self, config):
        self.host = config.server_ip_address
        self.port = config.server_port
        self.max_message_size = config.max_message_size
        self.socket = None
        self.users: set = set()
        self.users_lock = threading.Lock()

    def register_user(self, addr):
        with self.users_lock:
            self.users.add(addr)
        logging.info(f"{addr} registered successfully.")

    def unregister_user(self, addr):
        with self.users_lock:
            self.users.remove(addr)
        logging.info(f"{addr} unregistered successfully.")

    def start(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind((self.host, self.port))
        while True:
            data, addr = self.socket.recvfrom(self.max_message_size)
            self.process_data(data, addr)

    def send(self, data, addr):
        self.socket.sendto(data, addr)

    def process_data(self, data, source_addr):
        data_dict = json.loads(data.decode("utf-8"))
        message_type = data_dict.get("type")

        if message_type == MessageTypes.MESSAGE.value:
            logging.info(f"UDP - received message from {source_addr}")
            with self.users_lock:
                for addr in self.users:
                    if addr != source_addr:
                        self.send(data, addr)
        elif message_type == MessageTypes.REGISTER.value:
            self.register_user(source_addr)
        elif message_type == MessageTypes.UNREGISTER.value:
            self.unregister_user(source_addr)
        else:
            logging.error("Unsupported message type")

    def close(self):
        pass
