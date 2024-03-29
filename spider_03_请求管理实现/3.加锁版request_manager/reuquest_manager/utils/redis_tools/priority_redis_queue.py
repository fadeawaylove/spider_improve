import pickle
import threading

from .base import BaseRedisQueue


class PriorityRedisQueue(BaseRedisQueue):
    '''利用redis的有序集合来实现数据的存取'''

    def qsize(self):
        self.last_qsize = self.redis.zcard(self.name)
        return self.last_qsize

    def put_nowait(self, obj):
        '''
        :param obj: (score, value)
        :return:
        '''
        if self.lazy_limit and self.last_qsize < self.maxsize:
            pass
        elif self.full():
            raise self.Full

        self.last_qsize = self.redis.zadd(self.name, obj[0], pickle.dumps(obj[1]))
        return True

    def get_nowait(self):
        '''
        -1,-1: 默认取权重值最大的
        0,0：取权重最小的
        '''
        if self.use_lock is True:

            from .redis_lock import RedisLock
            if self.lock is None:
                self.lock = RedisLock(**self.redis_lock_config)

            if self.lock.acquire_lock():
                ret = self.redis.zrange(self.name, -1, -1)
                if not ret:
                    raise self.Empty

                self.redis.zrem(self.name, ret[0])
                self.lock.release_lock()

                return pickle.loads(ret[0])
        else:
            ret = self.redis.zrange(self.name, -1, -1)
            if not ret:
                raise self.Empty

            self.redis.zrem(self.name, ret[0])

            return pickle.loads(ret[0])



