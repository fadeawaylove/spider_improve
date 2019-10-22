import gevent
import time

now = lambda: time.time()


def test1():
    print("test1 start")
    gevent.sleep(1)  # 模拟IO事件，执行到此处时，gevent会自主交出当前协程的执行权
    print("test1 done")


def test2():
    print("test2 start")
    gevent.sleep(1)  # 模拟IO事件，执行到此处时，gevent会自主交出当前协程的执行权
    print("test2 done")


if __name__ == '__main__':
    start = now()

    gevent_greenlet1 = gevent.spawn(test1)
    gevent_greenlet2 = gevent.spawn(test2)

    gevent.joinall([
        gevent_greenlet1,
        gevent_greenlet2,
    ])

    print(now() - start)
