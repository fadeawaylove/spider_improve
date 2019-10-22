'''将事件放入线程池中执行'''

import asyncio
import time
import threading
import requests

now = lambda: time.time()


def event_handler(future):
    print("event_handler thread: ", threading.current_thread().name)
    if future:
        print("购买'%s'成功, 开始玩游戏" % future.result())
    else:
        print("购买失败")


# 事件函数
def buy(item):
    print("buy thread: ", threading.current_thread().name)
    return item


start = now()

# 获取默认的事件循环对象
loop = asyncio.get_event_loop()
# 使用run_in_executor： 注册事件event
# 默认buy会在一个线程池中运行
# future = loop.run_in_executor(None, requests.get, "http://www.baidu.com")
future = loop.run_in_executor(None, buy, "http://www.baidu.com")
future2 = loop.run_in_executor(None, buy, "http://www.baidu.com2")
# 设置回调函数，也就是event_handler
# 但回调还是主线程中运行
future.add_done_callback(event_handler)
# 启动事件循环
loop.run_until_complete(asyncio.wait([future, future2]))

print("耗时:", now() - start)
