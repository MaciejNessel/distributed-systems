import yaml

CONFIG_FILE_PATH = "config.yaml"


class Config:
    def __init__(self):
        with open(CONFIG_FILE_PATH) as f:
            config = yaml.load(f, Loader=yaml.FullLoader)
        self.server_host = config["server_host"]
        self.server_port = config["server_port"]
