import hashlib

import six
import redis


class MultipleHash(object):

    def __init__(self, salts, hash_func_name="md5"):
        self.hash_func = getattr(hashlib, hash_func_name)
        if len(salts) < 3:
            raise Exception("salts长度必须大于3！")
        self.salts = salts

    def get_hash_values(self, data):
        hash_values = []
        for salt in self.salts:
            hash_obj = self.hash_func()
            hash_obj.update(self._safe_data(data))
            hash_obj.update(self._safe_data(salt))
            hash_values.append(int(hash_obj.hexdigest(), 16))
        return hash_values

    @staticmethod
    def _safe_data(data):
        """
        将data预处理为可以进行hash处理的类型
        :param data:
        :return:
        """
        if six.PY3:
            if isinstance(data, str):
                return data.encode()
            elif isinstance(data, bytes):
                return data
            else:
                raise Exception("请提供一个字符串或者二进制")
        else:
            if isinstance(data, str):
                return data
            elif isinstance(data, unicode):
                return data.encode()
            else:
                raise Exception("请提供一个字符串或者unicode")


class BloomFilter(object):

    def __init__(self, *args, **kwargs):
        self.redis_host = kwargs.get("redis_host") or "localhost"
        self.redis_port = kwargs.get("redis_port") or 6379
        self.redis_db = kwargs.get("redis_db") or 0
        self.redis_key = kwargs.get("redis_key") or "bloomfilter"
        self.client = self._get_redis_client()
        self.multiple_hash = MultipleHash(kwargs.get("salts"), kwargs.get("hash_func_name") or "md5")
        if not self.multiple_hash:
            raise Exception("必须提供hash对象")

    def save(self, data):
        offsets = []
        for hash_value in self.multiple_hash.get_hash_values(data):
            offset = self._get_offset(hash_value)
            offsets.append(offset)
            self.client.setbit(self.redis_key, offset, 1)
        return offsets

    def is_exists(self, data):
        ret_list = []
        for hash_value in self.multiple_hash.get_hash_values(data):
            offset = self._get_offset(hash_value)
            ret_list.append(self.client.getbit(self.redis_key, offset))
        return all(ret_list)

    @staticmethod
    def _get_offset(hash_value):
        return hash_value % (128 * 1024 * 1024 * 8)

    def _get_redis_client(self):
        return redis.StrictRedis(
            connection_pool=redis.ConnectionPool(host=self.redis_host, port=self.redis_port, db=self.redis_db))


if __name__ == '__main__':
    b = BloomFilter(redis_host="172.17.0.4", hash_func_name="md5", salts=["a", "b", "c", "d"])
    b.save("我是你爸爸")
    print(b.is_exists("我是你爸爸"))
