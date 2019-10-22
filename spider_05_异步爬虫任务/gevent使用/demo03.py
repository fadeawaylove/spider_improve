# import gevent
import urllib.request

# 打补丁
import gevent.monkey

gevent.monkey.patch_all()


def test1():
    print("test1 start")
    # 网络I/O
    # 打补丁前，无法被gevent侦测到
    # 打补丁后，可以被gevent侦测到
    urllib.request.urlopen("http://www.baidu.com")
    print("test1 done")


def test2():
    print("test2 start")
    urllib.request.urlopen("http://www.baidu.com")
    print("test2 done")


if __name__ == '__main__':
    g1 = gevent.spawn(test1)
    g2 = gevent.spawn(test2)

    gevent.joinall([
        g1,
        g2,
    ])

'''运行结果：打补丁前，是同步的
test1 start
test1 done
test2 start
test2 done
'''

'''运行结果：打补丁后，是异步的
test1 start
test2 start
test2 done
test1 done
'''
