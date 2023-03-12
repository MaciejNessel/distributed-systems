import json
import logging
import socket
import threading

from utils.config import Config


class ServerUdp:
    def __init__(self):
        self.config = Config()
        self.host = self.config.server_url
        self.port = self.config.server_port
        self.socket = None
        self.users = {}
        self.users_lock = threading.Lock()

    def start(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind((self.host, self.port))
        print(f"Server listening on {self.host}:{self.port}")
        while True:
            data, addr = self.socket.recvfrom(self.config.max_message_size)
            print(data)
            # client_thread = threading.Thread(target=self.process_data, args=(conn, addr))
            # client_thread.start()
