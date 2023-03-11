import uuid
import logging

from client.client import Client
from utils.config import Config


class ClientTcp(Client):
    def connect(self):
        logging.info(f"Connecting to server...")

    def disconnect(self):
        logging.info(f"Disconnecting from server...")

    def send(self, message):
        pass

    def start(self):

        while True:
            command = input("")
            if command == "stop":
                self.stop()
                break

    def stop(self):
        pass
