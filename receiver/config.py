import msgspec


class Redis(msgspec.Struct):
    url: str

class Config(msgspec.Struct):
    redis: Redis