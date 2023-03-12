import json
import socket

from utils.config import Config


class ClientUdp:
    def __init__(self, port, server_url, server_port):
        self.config = Config()
        self.port = port
        self.__server_url = server_url
        self.__server_port = server_port
        self.__socket = self.init_socket()

    def init_socket(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind((self.__server_url, self.port))
        return sock

    def show_message(self, data):
        data = data.decode("utf-8")
        data = json.loads(data)
        print(
            "________________________________________________________________\n"
            f"# id: {data['id']}\n"
            f"# nick: {data['nick']}\n"
            f"# message:\n{data['content']}\n"
            "________________________________________________________________\n"
        )

    def listen(self):
        while True:
            data, address = self.__socket.recvfrom(self.config.max_message_size)
            if not data:
                break
            self.show_message(data)

    def send(self, data):
        self.__socket.sendto(data.encode(), (self.__server_url, self.__server_port))

    def close(self):
        self.__socket.close()
