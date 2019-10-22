'''asyncio多个事件异步执行1'''

import asyncio
import time

now = lambda: time.time()


def event_handler(future):
    if future:
        print("购买'%s'成功, 开始玩游戏" % future.result())
    else:
        print("购买失败")


# 1. 定义协程函数：购买手机的事件
async def buy(item):
    await asyncio.sleep(1)  #
    return item


start = now()

# 2. 获取默认的事件循环对象
loop = asyncio.get_event_loop()

tasks = []
for i in ["电脑", "手机", "掌机"]:
    # 3. 根据协程对象创建task对象: 注册事件event
    task = asyncio.ensure_future(buy(i))
    # 4.设置回调函数: 设置该事件的event_handler
    task.add_done_callback(event_handler)
    tasks.append(task)

# 5. 启动事件循环
loop.run_until_complete(asyncio.wait(tasks))

print("耗时:", now() - start)
