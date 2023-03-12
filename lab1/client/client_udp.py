import socket
import threading

from utils.message import show_message, prepare_message_to_read


class ClientUdp:
    def __init__(self, client_address, server_address, max_message_size):
        self.max_message_size = max_message_size
        self.client_address = client_address
        self.server_address = server_address
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.is_running = False

    def start(self):
        self.__socket.bind(self.client_address)
        self.is_running = True
        threading.Thread(target=self.listen, args=()).start()

    def listen(self):
        while self.is_running:
            try:
                data, address = self.__socket.recvfrom(self.max_message_size)
                if not data:
                    break
                message = prepare_message_to_read(data)
                show_message(message)
            except:
                break

    def send(self, data):
        self.__socket.sendto(data, self.server_address)

    def close(self):
        self.is_running = False
        self.__socket.close()
