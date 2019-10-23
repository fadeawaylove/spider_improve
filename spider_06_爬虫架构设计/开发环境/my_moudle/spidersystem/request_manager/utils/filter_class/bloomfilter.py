# 布隆过滤器 redis版本实现
import hashlib

import redis
import six

# 1. 多个hash函数的实现和求值
# 2. hash表实现和实现对应的映射和判断


class MultipleHash(object):
    '''根据提供的原始数据，和预定义的多个salt，生成多个hash函数值'''

    def __init__(self, salts, hash_func_name="md5"):
        self.hash_func = getattr(hashlib, hash_func_name)
        if len(salts) < 3:
            raise Exception("请至少提供3个salt")
        self.salts = salts

    def get_hash_values(self, data):
        '''根据提供的原始数据, 返回多个hash函数值'''
        hash_values = []
        for i in self.salts:
            hash_obj = self.hash_func()
            hash_obj.update(self._safe_data(data))
            hash_obj.update(self._safe_data(i))
            ret = hash_obj.hexdigest()
            hash_values.append(int(ret, 16))
        return hash_values

    def _safe_data(self, data):
        '''
        python2   str  === python3   bytes
        python2   uniocde === python3  str
        :param data: 给定的原始数据
        :return: 二进制类型的字符串数据
        '''
        if six.PY3:
            if isinstance(data, bytes):
                return data
            elif isinstance(data, str):
                return data.encode()
            else:
                raise Exception("请提供一个字符串")   # 建议使用英文来描述
        else:
            if isinstance(data, str):
                return data
            elif isinstance(data, unicode):
                return data.encode()
            else:
                raise Exception("请提供一个字符串")   # 建议使用英文来描述


class BloomFilter(object):
    ''''''
    def __init__(self, salts, redis_host="localhost", redis_port=6379, redis_db=0, redis_key="bloomfilter", *args, **kwargs):
        self.redis_host = redis_host
        self.redis_port = redis_port
        self.redis_db = redis_db
        self.redis_key = redis_key
        self.client = self._get_redis_client()
        self.multiple_hash = MultipleHash(salts)

    def _get_redis_client(self):
        '''返回一个redis连接对象'''
        pool = redis.ConnectionPool(host=self.redis_host, port=self.redis_port, db=self.redis_db)
        client = redis.StrictRedis(connection_pool=pool)
        return client

    def save(self, data):
        '''将原始数据在hash表中一一映射
        返回对应的偏移量'''
        hash_values = self.multiple_hash.get_hash_values(data)
        offsets = []
        for hash_value in hash_values:
            offset = self._get_offset(hash_value)
            offsets.append(str(offset))
            self.client.setbit(self.redis_key, offset, 1)
        return "-".join(offsets)

    def is_exists(self, data):
        hash_values = self.multiple_hash.get_hash_values(data)
        for hash_value in hash_values:
            offset = self._get_offset(hash_value)
            v = self.client.getbit(self.redis_key, offset)
            if v == 0:
                return False
        return True

    def _get_offset(self, hash_value):
        # 2**8 = 256
        # 2**20 = 1024 * 1024
        # 2 ** 31    256M
        # (2**8 * 2**20 * 2**3) 代表hash表的长度  如果同一项目中不能更改
        return hash_value % (2**8 * 2**20 * 2**3)


if __name__ == '__main__':

    data = ["asdfasdf", "123", "123", "456","asf", "asf"]

    bm = BloomFilter(salts=["1","2","3", "4"],redis_host="172.17.0.2")
    for d in data:
        if not bm.is_exists(d):
            bm.save(d)
            print("映射数据成功： ", d)
        else:
            print("发现重复数据：", d)


