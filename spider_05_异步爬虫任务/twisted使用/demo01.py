import time

from twisted.internet import reactor

now = lambda: time.time()

def task(x):
    print('The Number Is :', x)
    time.sleep(0.1)
    if x == 9:
        # 退出事件循环
        reactor.stop()

start = now()
for i in range(10):
    reactor.callWhenRunning(task, i)

print(dir(reactor))
# 启动事件循环
reactor.run()

print("耗时:", now()-start)

'''运行结果
The Number Is : 0
The Number Is : 1
The Number Is : 2
The Number Is : 3
The Number Is : 4
The Number Is : 5
The Number Is : 6
The Number Is : 7
The Number Is : 8
The Number Is : 9
耗时: 1.0598435401916504
'''