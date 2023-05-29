import asyncio
import json

import toml
import msgpack
import redis.asyncio as aioredis

from rover import Rover

class RedisPubSubReceiver:
    def __init__(self):
        config = toml.load("config.toml")
        redis_url = config["redis"]["url"]
        self.redis = aioredis.from_url(redis_url)
        self.pubsub = self.redis.pubsub()

        self.rover = Rover()

    async def receive(self):
        await self.pubsub.subscribe("pathfinder")
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
        motor = getattr(self.rover, f"{motor}_motor")
        func = getattr(motor, direction)
        func(speed)



receiver = RedisPubSubReceiver()
asyncio.run(receiver.receive())