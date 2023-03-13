import socket
import struct
import threading

from utils.message import show_message, prepare_message_to_read


class ClientMulticast:
    def __init__(self, multicast_group, multicast_port, max_message_size):
        self.max_message_size = max_message_size
        self.multicast_group = multicast_group
        self.multicast_port = multicast_port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)

    def start(self):
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind(("", self.multicast_port))

        # Add membership to multicast group
        group = socket.inet_aton(self.multicast_group)
        self.socket.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, struct.pack("4sL", group, socket.INADDR_ANY))

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
        self.socket.sendto(data, (self.multicast_group, self.multicast_port))

    def stop(self):
        self.socket.close()
