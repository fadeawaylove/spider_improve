'''显示退出循环'''

import asyncio
import time

now = lambda: time.time()


# 1. 定义协程函数
async def task1():
    print("task1 start")
    await asyncio.sleep(5)
    print("task1 done")


async def task2():
    print("task2 start")
    await asyncio.sleep(1)
    print("task2 done")


def callback(future):
    loop.stop()


start = now()

# 获取默认的事件循环对象
loop = asyncio.get_event_loop()
# 注册task
task1 = asyncio.Task(task1())
task2 = asyncio.Task(task2())
task2.add_done_callback(callback)  # task2执行完毕，立刻关闭循环

# 启动事件循环：

# 由于还有任务没完成，stop后，run_until_complete会抛出异常
# loop.run_until_complete(asyncio.wait([task1,task2]))

# 而loop.stop会在run_forever的合适时候退出
loop.run_forever()

print("耗时:", now() - start)
