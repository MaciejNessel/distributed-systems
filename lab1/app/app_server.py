import logging

from server.server import Server


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    logging.info("Initializing server...")
    server = Server()
    server.start()
