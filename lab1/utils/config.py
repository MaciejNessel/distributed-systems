import yaml

CONFIG_FILE_PATH = "config.yaml"


class Config:
    def __init__(self):
        with open(CONFIG_FILE_PATH) as f:
            config = yaml.load(f, Loader=yaml.FullLoader)
        self.server_ip_address = config["server_ip_address"]
        self.server_port = config["server_port"]
        self.client_ip_address = config["client_ip_address"]
        self.max_message_size = config["max_message_size"]
        self.client_default_mode = config["client_default_mode"]
        self.multicast_group = config["multicast_group"]
        self.multicast_port = config["multicast_port"]
