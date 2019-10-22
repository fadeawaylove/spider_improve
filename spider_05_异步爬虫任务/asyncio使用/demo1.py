'''asyncio事件驱动使用'''

import asyncio
import time

now = lambda: time.time()


# callback：事件处理器
def event_handler(future):
    if future:
        print("购买'%s'成功, 开始玩游戏" % future.result())
    else:
        print("购买失败")


# 1. 定义协程函数：购买事件
async def buy(item):
    return item


start = now()

# 2. 调用协程函数获得协程对象
coroutine = buy("电脑")
# 3. 获取默认的事件循环对象
loop = asyncio.get_event_loop()
# 4. 根据协程对象创建task对象: 注册事件event
# task = loop.create_task(coroutine)
task = asyncio.ensure_future(coroutine)
# task = asyncio.Task(coroutine)
# 5.设置回调函数，也就是event_handler
task.add_done_callback(event_handler)
print(task)

# 6. 启动事件循环
loop.run_until_complete(task)

print(task)
print("耗时:", now() - start)
