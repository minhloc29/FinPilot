class CacheManager:

    def __init__(self, redis_cache):
        self.redis = redis_cache

    def get(self, key):
        return self.redis.get(key)

    def set(self, key, value):
        self.redis.set(key, value)