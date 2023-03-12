import socket
import struct
import threading

from utils.message import show_message, prepare_message_to_read


class ClientMulticast:
    def __init__(self, multicast_group, multicast_port, max_message_size):
        self.max_message_size = max_message_size
        self.multicast_address = multicast_group
        self.multicast_port = multicast_port
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.is_running = False

    def start(self):
        ttl = struct.pack("b", 1)
        self.__socket.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)
        self.__socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        self.__socket.bind(("", self.multicast_port))

        # Add membership to multicast group
        group = socket.inet_aton(self.multicast_address)
        self.__socket.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, struct.pack("4sL", group, socket.INADDR_ANY))

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
        self.__socket.sendto(data, (self.multicast_address, self.multicast_port))

    def close(self):
        self.is_running = False
        self.__socket.close()
