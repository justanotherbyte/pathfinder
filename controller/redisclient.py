import msgspec
import msgpack
import redis

from message import RedisMessage


class RedisConfig(msgspec.Struct):
    url: str

class Config(msgspec.Struct):
    redis: RedisConfig

class Redis:
    def __init__(self):
        with open("config.toml", "r") as f:
            contents = f.read()
        
        config = msgspec.toml.decode(contents, type=Config)
        self.redis = redis.from_url(config.redis.url)

    def send(self, *messages: RedisMessage):
        for message in messages:
            data = msgspec.json.encode(message)
            data = msgpack.dumps(data)
            self.redis.publish("pathfinder", data) # type: ignore

    