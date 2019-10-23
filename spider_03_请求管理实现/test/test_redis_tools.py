from redis_tools import get_redis_queue_cls, get_redis_lock_cls

redis_lock = get_redis_lock_cls()("lock1", host="172.17.0.4")

q = get_redis_queue_cls("priority")(name="priority_key", host='172.17.0.4', port=6379, db=0, redis_lock=redis_lock)

# for i in range(10):
#     q.put(("value" + str(i), i))

print(q.get())
