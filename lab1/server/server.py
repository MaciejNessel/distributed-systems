import signal
import threading

from server_tcp import ServerTcp
from server_udp import ServerUdp


class Server:
    def __init__(self):
        self.is_running = True
        self.server_tcp = None
        self.server_udp = None

    def start(self):
        self.server_tcp = ServerTcp()
        self.server_udp = Serv()
        threading.Thread(target=self.server_tcp.start, daemon=True).start()
        threading.Thread(target=self.server_udp.start, daemon=True).start()

        signal.signal(signal.SIGINT, self.stop)
        while self.is_running:
            pass

    def stop(self):
        self.server_tcp.close()
        self.server_udp.close()
