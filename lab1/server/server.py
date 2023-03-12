import logging
import signal
import threading
import time

from server.server_tcp import ServerTcp
from server.server_udp import ServerUdp
from utils.config import Config


class Server:
    def __init__(self):
        self.is_running = True
        self.server_tcp = None
        self.server_udp = None
        self.config = Config()

    def start(self):
        self.server_tcp = ServerTcp(self.config)
        self.server_udp = ServerUdp(self.config)

        threading.Thread(target=self.server_tcp.start, daemon=True).start()
        threading.Thread(target=self.server_udp.start, daemon=True).start()

        logging.info(f"Server TCP listening on {self.config.server_url}:{self.config.server_port}")
        signal.signal(signal.SIGINT, self.stop)
        while self.is_running:
            command = input("#")
            if "--close" == command:
                self.stop()
            else:
                logging.error(f"Unsupported command: '{command}'")

    def stop(self):
        self.server_tcp.close()
        self.server_udp.close()
        logging.info("Finished shutting down")
        self.is_running = False
