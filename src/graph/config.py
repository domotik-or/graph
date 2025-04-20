from pathlib import Path
import tomllib

from graph.typem import DeviceConfig
from graph.typem import ServerConfig

device = None
server = None


def read(config_filename: str):
    config_file = Path(config_filename)
    with open(config_file, "rb") as f:
        raw_config = tomllib.load(f)

    global device
    device = DeviceConfig()
    for k, v in raw_config["device"].items():
        setattr(device, k, v)

    global server
    server = ServerConfig(**raw_config["server"])
