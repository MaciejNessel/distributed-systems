import socket


class ClientTcp:
    def __init__(self, server_url, server_port):
        self.__server_url = server_url
        self.__server_port = server_port
        self.__socket = self.init_socket()

    def init_socket(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((self.__server_url, self.__server_port))
        return sock

    def send(self, data):
        self.__socket.sendall(data.encode())
        response = self.__socket.recv(1024)
        return response.decode()

    def close(self):
        self.__socket.close()
