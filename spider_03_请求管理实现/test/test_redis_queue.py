"""测试redis各种队列"""
import random
import time
import unittest

from redis_tools import get_redis_queue_cls


class TestQueue(unittest.TestCase):

    def test_redis_priority_queue(self):
        """
        测试redis优先级队列
        :return:
        """
        redis_queue_cls = get_redis_queue_cls("priority")
        q = redis_queue_cls(name="priority_key", host='192.168.219.3', port=6379, db=1)
        for x in range(10):
            q.put(("value" + str(x), random.randint(1, 20)))
        time.sleep(3)
        while True:
            print(q.get())
            time.sleep(0.1)

    def test_redis_fifo_queue(self):
        """
        将数据取出队列
        :return:
        """
        redis_queue_cls = get_redis_queue_cls("fifo")
        q = redis_queue_cls(name='fifo', host='192.168.219.3', port=6379, db=1)
        for x in range(10):
            q.put(f"value{x}")
        time.sleep(3)
        while True:
            print(q.get())

    def test_redis_filo_queue(self):
        """
        将数据取出队列
        :return:
        """
        redis_queue_cls = get_redis_queue_cls("lifo")
        q = redis_queue_cls(name='lifo', host='192.168.219.3', port=6379, db=1)
        for x in range(10):
            q.put(f"value{x}")
        time.sleep(3)
        while True:
            print(q.get())
