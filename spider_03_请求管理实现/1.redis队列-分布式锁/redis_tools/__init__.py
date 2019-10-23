def get_redis_lock_cls():
    """
    获取redis锁类
    :return:
    """
    from .redis_lock import RedisLock
    return RedisLock


def get_redis_queue_cls(queue_name="fifo"):
    if queue_name == "fifo":
        from .fifo_redis_queue import FifoRedisQueue
        return FifoRedisQueue
    if queue_name == "lifo":
        from .lifo_redis_queue import LifoRedisQueue
        return LifoRedisQueue
    if queue_name == "priority":
        from .priority_redis_queue import PriorityRedisQueue
        return PriorityRedisQueue
    raise Exception("redis queue: [{}] don't exists!".format(queue_name))
