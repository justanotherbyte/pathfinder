import redis.asyncio as aioredis

class RedisPubSubReceiver:
    def __init__(self):
        self.redis = aioredis.from_url()