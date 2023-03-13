import socket
import threading

from utils.message import show_message, prepare_message_to_read


class ClientUdp:
    def __init__(self, client_address, server_address, max_message_size):
        self.max_message_size = max_message_size
        self.client_address = client_address
        self.server_address = server_address
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def start(self):
        self.socket.bind(self.client_address)
        threading.Thread(target=self.listen, args=()).start()

    def listen(self):
        while True:
            try:
                data, address = self.socket.recvfrom(self.max_message_size)
                if not data:
                    break
                message = prepare_message_to_read(data)
                show_message(message)
            except socket.error:
                break

    def send(self, data):
        self.socket.sendto(data, self.server_address)

    def stop(self):
        self.socket.close()
