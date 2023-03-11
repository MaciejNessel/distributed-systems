import socket
import threading

from utils.config import Config


class Server:
    def __init__(self):
        config = Config()
        self.host = config.server_url
        self.port = config.server_port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def start(self):
        self.socket.bind((self.host, self.port))
        self.socket.listen()
        print(f"Server listening on {self.host}:{self.port}")
        while True:
            conn, addr = self.socket.accept()
            print(f"New client connected from {addr}")
            client_thread = threading.Thread(target=self.handle_client, args=(conn,))
            client_thread.start()

    def handle_client(self, conn):
        with conn:
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                # process data from client
                response = self.process_data(data)
                conn.sendall(response)

    def process_data(self, data):
        print(data)
        # do something with the data received from client
        return data.upper()
