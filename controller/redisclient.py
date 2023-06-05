import json
from threading import Thread

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
        self.pubsub = self.redis.pubsub()
        self.pubsub.subscribe("pathfinder:distance")

        self.receiving = True

        thread = Thread(target=self.receive, daemon=True)
        thread.start()

    def send(self, *messages: RedisMessage):
        for message in messages:
            data = msgspec.json.encode(message)
            data = msgpack.dumps(data)
            self.redis.publish("pathfinder:movement", data) # type: ignore

    def receive(self):
        while self.receiving:
            message = self.pubsub.get_message(
                ignore_subscribe_messages=True
            )
            if message:
                data = message.get("data")
                if data:
                    unpacked = msgpack.loads(data)
                    parsed = json.loads(unpacked)
                    self.handle_distance_message(parsed)
    
    def handle_distance_message(self, message: dict):
        print(message)