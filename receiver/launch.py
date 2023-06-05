import asyncio
import json

import toml
import msgpack
import msgspec
import redis.asyncio as aioredis

from rover import Rover
from config import Config


class RedisPubSubReceiver:
    def __init__(self):
        with open("config.toml", "r") as f:
            contents = f.read()
        
        config = msgspec.toml.decode(contents, type=Config)
        self.redis = aioredis.from_url(config.redis.url)
        self.pubsub = self.redis.pubsub()

        self.rover = Rover()

    async def receive(self):
        await self.pubsub.subscribe("pathfinder:movement")
        while True:
            message = await self.pubsub.get_message(True)
            if message:
                data = message.get("data")
                if data:
                    unpacked = msgpack.loads(data)
                    print(unpacked)
                    parsed = json.loads(unpacked)
                    self.handle_message(parsed)
    
    def handle_message(self, data: dict):
        speed = data["speed"]
        direction = data["direction"].lower()
        motor = data["motor"].lower()
        if motor == "both":
            right_func = getattr(self.rover.right_motor, direction)
            left_func = getattr(self.rover.left_motor, direction)
            right_func(speed)
            left_func(speed)
        else:
            motor = getattr(self.rover, f"{motor}_motor")
            func = getattr(motor, direction)
            func(speed)



receiver = RedisPubSubReceiver()
asyncio.run(receiver.receive())