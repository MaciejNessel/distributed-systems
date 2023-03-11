import uuid
import logging

from utils.config import Config


class Client:
    def __init__(self, nick, port):
        self.nick = nick
        self.port = port
        self.id = uuid.uuid4()
        self.config = Config()

        self.start()

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
