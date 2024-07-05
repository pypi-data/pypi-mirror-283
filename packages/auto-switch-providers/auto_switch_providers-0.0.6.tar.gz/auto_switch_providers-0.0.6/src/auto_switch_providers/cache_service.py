from json import dumps
from time import perf_counter
from typing import Union

from .services.redis_service import RedisClient


class CacheService:
    def __init__(self, config: dict = None) -> None:
        self.client = None
        if config is not None:
            self.config = config
            self.database = config.get("database") if config.get("database") else ""

            # expires_in: A numeric value is interpreted as a seconds count.
            default_expires_in = 604800
            expires_in = (
                config.get("expires_in")
                if config.get("expires_in")
                else default_expires_in
            )
            if not isinstance(expires_in, int):
                expires_in = int(expires_in)
            if not expires_in:
                expires_in = default_expires_in
            self.expires_in = expires_in

            start_time = perf_counter()
            self.client = RedisClient(self.config).get_client()
            if self.client:
                try:
                    self.client.ping()
                    self.status = True
                    exec_time = perf_counter() - start_time
                    host_name = self.config.get("host")
                    print(
                        f"⚡️ Redis enabled! (ping: {exec_time*1000:.2f} ms, host: {host_name})"
                    )
                except Exception:
                    self.status = False
                    print("⛔️ Redis disabled!")
                    print(dumps(self.config))
                    pass

    def _key(self, keys: Union[str, list]):
        if isinstance(keys, str):
            return keys
        return ":".join(keys)

    def _prefix(self):
        prefix = self.database if self.database and self.database != "" else None
        if not prefix:
            return ""
        if prefix.endswith(":"):
            return prefix
        return f"{prefix}:"

    def exists(self, key: Union[str, list]):
        return self.client.exists(f"{self._prefix()}{self._key(key)}")

    def hget(self, hash: str, key: str):
        return self.client.hget(f"{self._prefix()}{self._key(hash)}", key)

    def hset(self, hash: str, key: str, value: Union[str, list, dict]):
        self.client.hset(f"{self._prefix()}{self._key(hash)}", key, dumps(value))
        self.client.expire(f"{self._prefix()}{self._key(hash)}", time=self.expires_in)
