import socket
import threading

from utils.message import prepare_message_to_read, show_message


class ClientTcp:
    def __init__(self, client_address, server_address, max_message_size):
        self.max_message_size = max_message_size
        self.client_address = client_address
        self.server_address = server_address
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def start(self):
        self.socket.bind(self.client_address)
        self.socket.connect(self.server_address)
        threading.Thread(target=self.listen, args=()).start()

    def listen(self):
        while True:
            try:
                data = self.socket.recv(self.max_message_size)
                if not data:
                    break
                message = prepare_message_to_read(data)
                show_message(message)
            except socket.error:
                break

    def send(self, data):
        self.socket.sendall(data)

    def stop(self):
        # self.socket.shutdown(socket.SHUT_RDWR)
        self.socket.close()
