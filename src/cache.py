from redis import Redis
from src.config import settings


class Cache:
    def __init__(self, host="localhost", port=6379):
        self.client = Redis(host=host, port=port)

    def set(self, key, value):
        self.client.set(key, value)

    def get(self, key):
        return self.client.get(key)


cache = Cache(host=settings.REDIS_HOST, port=settings.REDIS_PORT)
