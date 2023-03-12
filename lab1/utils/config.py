import yaml

CONFIG_FILE_PATH = "config.yaml"


class Config:
    def __init__(self):
        with open(CONFIG_FILE_PATH) as f:
            config = yaml.load(f, Loader=yaml.FullLoader)
        self.server_url = config["server_url"]
        self.server_port = config["server_port"]
        self.max_message_size = config["max_message_size"]
