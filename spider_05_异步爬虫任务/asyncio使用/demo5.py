'''协程嵌套之链式嵌套'''

import asyncio
import time

now = lambda: time.time()


# 1. 定义协程函数
async def task0():
    await asyncio.sleep(1)
    print("task0 done")


async def task1():
    await asyncio.sleep(1)
    print("task1 done")


async def task2():
    await asyncio.sleep(1)
    print("task2 done")


async def task3():
    await task0()
    await task1()
    await task2()
    await asyncio.sleep(1)
    print("task3 done")


start = now()

# 获取默认的事件循环对象
loop = asyncio.get_event_loop()
# 获取task对象
task = asyncio.Task(task3())
# 启动事件循环
loop.run_until_complete(task)

print("耗时:", now() - start)
