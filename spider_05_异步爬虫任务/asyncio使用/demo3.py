'''asyncio多个事件异步执行2'''

import asyncio
import time
import random
import threading

now = lambda: time.time()


def event_handler(future):
    print("event_handler: ", threading.current_thread().name)
    if future:
        print("购买'%s'成功, 开始玩游戏" % future.result())
    else:
        print("购买失败")


# 1. 定义协程函数：购买手机的事件
async def buy(item):
    print("buy: ", threading.current_thread().name)
    await asyncio.sleep(random.randint(0, 10) * 0.1)
    return item


start = now()

# 2. 获取默认的事件循环对象
loop = asyncio.get_event_loop()
tasks = []
for i in ["电脑", "手机", "掌机", "a1", 'a2', "a3"]:
    # 3. 根据协程对象创建task对象: 注册事件event
    task = asyncio.ensure_future(buy(i))
    # 4.设置回调函数: 设置该事件的event_handler
    task.add_done_callback(event_handler)
    tasks.append(task)
# 5. 启动事件循环
loop.run_until_complete(asyncio.wait(tasks))
print("耗时:", now() - start)
