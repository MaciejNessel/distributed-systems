import json
import socket

from utils.config import Config


class ClientTcp:
    def __init__(self, server_url, server_port):
        self.config = Config()
        self.__server_url = server_url
        self.__server_port = server_port
        self.__socket = self.init_socket()

    def init_socket(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((self.__server_url, self.__server_port))
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
            data = self.__socket.recv(self.config.max_message_size)
            if not data:
                break
            self.show_message(data)

    def send(self, data):
        self.__socket.sendall(data.encode())

    def close(self):
        try:
            self.__socket.shutdown(socket.SHUT_RDWR)
        except OSError:
            pass
        finally:
            self.__socket.close()
