import json
import logging
import socket
import threading

from common.message import MessageTypes


class ServerTcp:
    def __init__(self, config):
        self.server_address = (config.server_ip_address, config.server_port)
        self.max_message_size = config.max_message_size

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.users = {}
        self.users_lock = threading.Lock()

    def start(self):
        self.socket.bind(self.server_address)
        self.socket.listen()
        threading.Thread(target=self.listen, daemon=True).start()

    def listen(self):
        while True:
            conn, addr = self.socket.accept()
            logging.info(f"New client connected from {addr}")
            client_thread = threading.Thread(target=self.handle_client, args=(conn, addr))
            client_thread.start()

    def register_user(self, conn, addr):
        with self.users_lock:
            self.users[addr] = conn
        logging.info(f"TCP {addr} registered successfully.")

    def unregister_user(self, addr):
        with self.users_lock:
            self.users.pop(addr)
        logging.info(f"TCP {addr} unregistered successfully.")

    def handle_client(self, conn, addr):
        with conn:
            try:
                while True:
                    data = conn.recv(self.max_message_size)
                    if not data:
                        break
                    self.process_data(data, conn, addr)
            except socket.error:
                return
            finally:
                conn.close()
                logging.info(f"Client {addr} terminated successfully")

    def process_data(self, data, conn, source_addr):
        data_dict = json.loads(data.decode("utf-8"))
        message_type = data_dict.get("type")

        if message_type == MessageTypes.MESSAGE.value:
            logging.info(f"TCP - received message from {source_addr}")
            with self.users_lock:
                for addr, conn in self.users.items():
                    if addr != source_addr:
                        conn.sendall(data)
        elif message_type == MessageTypes.REGISTER.value:
            self.register_user(conn, source_addr)
        elif message_type == MessageTypes.UNREGISTER.value:
            self.unregister_user(source_addr)
        else:
            logging.error("Unsupported message type")

    def close(self):
        for addr, conn in self.users.items():
            conn.close()
        self.users.clear()
        logging.info("Server TCP closed successfully.")
