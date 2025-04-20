from dataclasses import dataclass
# from enum import auto
# from enum import Enum
# from enum import IntEnum


class DeviceConfig:
    pass


@dataclass
class ServerConfig:
    hostname: str
    port: int
