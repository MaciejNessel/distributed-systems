import logging

from server.server import Server
from utils.config import Config

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    logging.info("Initializing server...")
    config = Config()
    server = Server(config)
    server.start()
