'''task 任务取消'''
import asyncio
import time

now = lambda: time.time()


# 1. 定义协程函数
async def task0():
    print("task0 start")
    await asyncio.sleep(5)
    print("task0 done")


async def cancel_task(task):
    await asyncio.sleep(1)
    print("取消前: ", task)
    task.cancel()
    print("取消后: ", task)


start = now()

# 获取默认的事件循环对象
loop = asyncio.get_event_loop()
# 获取task对象
main_task = asyncio.Task(task0())
# 启动事件循环
# 1秒后，main_task将被取消
loop.run_until_complete(asyncio.wait([main_task, cancel_task(main_task)]))
print("耗时:", now() - start)
