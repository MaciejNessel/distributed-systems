import logging
import signal
import sys

from server.server_tcp import ServerTcp
from server.server_udp import ServerUdp


class Server:
    def __init__(self, config):
        self.is_running = True
        self.config = config
        self.server_tcp = ServerTcp(self.config)
        self.server_udp = ServerUdp(self.config)

    def start(self):
        self.server_tcp.start()
        self.server_udp.start()

        signal.signal(signal.SIGINT, self.stop)

        logging.info(f"Server TCP listening on {self.config.server_ip_address}:{self.config.server_port}")
        while True:
            continue

    def stop(self, sig, frame):
        self.server_tcp.close()
        self.server_udp.close()
        logging.info("Finished shutting down")
        sys.exit(0)
