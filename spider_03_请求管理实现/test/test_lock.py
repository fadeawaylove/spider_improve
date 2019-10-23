from redis_tools.redis_lock import RedisLock

redis_lock = RedisLock("lock1", host="192.168.219.3")

print(redis_lock.acquire_lock(expire_time=10))
print("代码操作")
# print(redis_lock.release_lock())
