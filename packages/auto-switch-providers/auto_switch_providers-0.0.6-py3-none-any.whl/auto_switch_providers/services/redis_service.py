from redis import Redis, StrictRedis


class RedisClient:
    def __init__(self, config=None):
        self.config = config or {}
        if config and config.get("password"):
            self.redis_client = StrictRedis(
                host=self.config.get("host", "127.0.0.1"),
                port=self.config.get("port", 6379),
                password=self.config.get("password", ""),
                decode_responses=True,
            )
        else:
            self.redis_client = Redis(
                host=self.config.get("host", "127.0.0.1"),
                port=self.config.get("port", 6379),
                decode_responses=True,
            )

    def get_client(self):
        return self.redis_client
