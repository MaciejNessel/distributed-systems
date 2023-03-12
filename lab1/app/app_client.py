import logging
import sys

from client.client import Client
from utils.config import Config

if __name__ == "__main__":
    if len(sys.argv) == 3:
        config = Config()
        nick = sys.argv[1]
        port = int(sys.argv[2])
        c = Client(nick, port, config)
        c.start()

    else:
        logging.error("Wrong number of arguments")
