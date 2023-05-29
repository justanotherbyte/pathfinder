import asyncio

import toml
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
        message = await self.pubsub.get_message(True)
        print(message)
    
    def start(self):
        asyncio.create_task(self.receive())


RedisPubSubReceiver().start()