import umsgpack

from .base import BaseRedisQueue


class PriorityRedisQueue(BaseRedisQueue):

    def qsize(self):
        self.last_qsize = self.redis.zcard(self.name)
        return self.last_qsize

    def put_nowait(self, obj):
        """
        :param obj: obj[0]=score obj[1]=value
        :return:
        """
        if self.lazy_limit and self.last_qsize < self.maxsize:
            pass
        elif self.full():
            raise self.Full
        # zadd("xxx", {"value5":5})
        self.last_qsize = self.redis.zadd(self.name, {umsgpack.packb(obj[0]): obj[1]})
        return True

    def get_nowait(self):
        if self.redis_lock:
            # 执行有锁版本
            while True:
                if self.redis_lock.acquire_lock():
                    ret = self.redis.zpopmax(self.name, 1)
                    break
        else:
            ret = self.redis.zpopmax(self.name, 1)

        if not ret:
            raise self.Empty
        return umsgpack.unpackb(ret[0][0]), ret[0][1]
