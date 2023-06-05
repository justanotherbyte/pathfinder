from enum import Enum

import msgspec


class Direction(Enum):
    Forward = "forward"
    Backward = "backward"

class Motor(Enum):
    Both = "both"
    Left = "left"
    Right = "right"


class RedisMessage(msgspec.Struct):
    direction: Direction
    motor: Motor
    speed: float
