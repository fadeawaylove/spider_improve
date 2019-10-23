import os
import socket
import pickle
import time

import redis


class RedisLock(object):

    def __init__(self, lock_name, host="localhost", port=6379, db=0):
        self.redis = redis.StrictRedis(host=host, port=port, db=db)
        self.lock_name = lock_name

    def _get_thread_id(self):
        return "{}-{}".format(socket.gethostname(), os.getpid())

    def acquire_lock(self, thread_id=None, expire_time=10, block=True):
        """
        获取锁成功返回True，否则返回失败
        :param thread_id:
        :param expire_time:
        :param block:
        :return:
        """
        if thread_id is None:
            thread_id = self._get_thread_id()
        while block:
            ret = self.redis.setnx(self.lock_name, pickle.dumps(thread_id))
            if ret == 1:
                self.redis.expire(self.lock_name, expire_time)
                return True
            time.sleep(0.01)

        ret = self.redis.setnx(self.lock_name, pickle.dumps(thread_id))
        if ret == 1:
            self.redis.expire(self.lock_name, expire_time)
            return True
        else:
            return False

    def release_lock(self, thread_id=None):
        """
        获取锁之后比较thread_id，如果相同才能解锁成功
        :param thread_id:
        :return:
        """
        if thread_id is None:
            thread_id = self._get_thread_id()
        ret = self.redis.get(self.lock_name)
        if ret and pickle.loads(ret) == thread_id:
            self.redis.delete(self.lock_name)
            return True
        else:
            return False
