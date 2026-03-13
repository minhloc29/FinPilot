import time


class QuoteCache:

    def __init__(self, ttl=60):
        self.cache = {}
        self.ttl = ttl

    def get(self, key):

        if key in self.cache:

            data, timestamp = self.cache[key]

            if time.time() - timestamp < self.ttl:
                return data

            del self.cache[key]

        return None

    def set(self, key, data):

        self.cache[key] = (data, time.time())