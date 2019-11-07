from . import BaseFilter

import redis


class RedisFilter(BaseFilter):

    def __init__(self, *args, **kwargs):
        self.redis_host = kwargs.get("redis_host") or "localhost"
        self.redis_port = kwargs.get("redis_port") or 6379
        self.redis_db = kwargs.get("redis_db") or 0
        self.redis_key = kwargs.get("redis_key") or "filter"
        super(RedisFilter, self).__init__(*args, **kwargs)

    def _save(self, hash_value):
        return self.storage.sadd(self.redis_key, hash_value)

    def _is_exists(self, hash_value):
        return self.storage.sismember(self.redis_key, hash_value)

    def _get_storage(self):
        return redis.StrictRedis(
            connection_pool=redis.ConnectionPool(host=self.redis_host, port=self.redis_port, db=self.redis_db))
