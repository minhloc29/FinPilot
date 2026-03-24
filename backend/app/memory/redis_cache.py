import redis

class RedisCache:

    def __init__(self, host="localhost", port=6379, db=0):
        self.client = redis.Redis(
            host=host,
            port=port,
            db=db,
            decode_responses=True
        )

    def get(self, key: str):
        return self.client.get(key)

    def set(self, key: str, value: str, ttl: int = 3600):
        self.client.set(key, value, ex=ttl)