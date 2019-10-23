import time
from .base import BaseRedisQueue

import umsgpack


class LifoRedisQueue(BaseRedisQueue):

    def get_nowait(self):
        ret = self.redis.rpop(self.name)
        if ret is None:
            raise self.Empty
        return umsgpack.unpackb(ret)
