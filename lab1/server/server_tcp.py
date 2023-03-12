import json
import logging
import socket
import threading

from utils.config import Config


class ServerTcp:
    def __init__(self):
        self.config = Config()
        self.host = self.config.server_url
        self.port = self.config.server_port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.users = {}
        self.users_lock = threading.Lock()

    def start(self):
        self.socket.bind((self.host, self.port))
        self.socket.listen()
        print(f"Server listening on {self.host}:{self.port}")
        while True:
            conn, addr = self.socket.accept()
            print(f"New client connected from {addr}")
            client_thread = threading.Thread(
                target=self.handle_client, args=(conn, addr)
            )
            client_thread.start()

    def register_user(self, conn, addr):
        self.users_lock.acquire()
        self.users[addr] = conn
        self.users_lock.release()
        logging.info(f"{addr} registered successfully.")

    def unregister_user(self, addr):
        self.users_lock.acquire()
        self.users.pop(addr)
        self.users_lock.release()
        logging.info(f"{addr} unregistered successfully.")

    def handle_client(self, conn, addr):
        with conn:
            self.register_user(conn, addr)
            try:
                while True:
                    data = conn.recv(self.config.max_message_size)
                    if not data:
                        break
                    self.process_data(data, addr)
            except Exception as e:
                print(f"An error occurred while processing client request: {e}")
            finally:
                conn.close()
                self.unregister_user(addr)
                print(f"Client {addr} terminated successfully")

    def process_data(self, data, source_addr):
        self.users_lock.acquire()
        for addr, conn in self.users.items():
            if addr != source_addr:
                conn.sendall(data)
        self.users_lock.release()
