'''协程嵌套之组合嵌套'''

import asyncio
import time

now = lambda: time.time()


# 1. 定义协程函数
async def task0():
    await asyncio.sleep(1)
    print("task0 done")
    return "task0"


async def task1():
    await asyncio.sleep(1)
    print("task1 done")
    return "task1"


async def task2():
    await asyncio.sleep(1)
    print("task2 done")
    return "task2"


async def task3():
    await asyncio.sleep(1)
    print("task3 done")
    return "task3"


async def main():
    tasks = [task0(),
             task1(),
             task2(),
             task3()]

    # 有三种方式进行协程组合嵌套
    # 1. asyncio.wait
    # dones, pendings = await asyncio.wait(tasks)
    # for task in dones:
    #     print(task.result())
    '''运行结果: 异步运行、异步输出
    task3 done
    task1 done
    task0 done
    task2 done
    task2
    task0
    task3
    task1
    耗时: 1.0027110576629639
    '''

    # 2. asyncio.as_completed
    # for task in asyncio.as_completed(tasks):
    #     result = await task
    #     print(result)
    '''运行结果: 异步运行、异步输出，执行顺序和结果顺序一致
    task2 done
    task1 done
    task3 done
    task0 done
    task2
    task1
    task3
    task0
    耗时: 1.0028691291809082
    '''

    # 3. asyncio.gather
    # results = await asyncio.gather(*tasks)
    # print(results)
    '''运行结果: 异步运行、同步输出，结果顺序和传参顺序一致
    task0 done
    task1 done
    task2 done
    task3 done
    ['task0', 'task1', 'task2', 'task3']
    耗时: 1.0031750202178955
    '''


start = now()

# 获取默认的事件循环对象
loop = asyncio.get_event_loop()
# 获取task对象
main_task = asyncio.Task(main())
# 启动事件循环
loop.run_until_complete(main_task)
print("耗时:", now() - start)
