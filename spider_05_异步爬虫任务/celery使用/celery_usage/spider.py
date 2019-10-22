import time
import tasks

now = lambda: time.time()


def use_celery():
    '''通过delay方法传参调用，才会将函数交由celery进行异步处理'''
    start = now()
    url = "http://www.baidu.com/s?wd="
    rets = []
    for i in range(10):
        ret = tasks.urlopen.delay(url + str(i))
        print(ret)
        rets.append(ret)
    print("耗时：", now() - start)


def no_celery():
    '''如果直接调用函数，那么将不会交由celery处理'''

    start = now()
    url = "http://www.baidu.com/s?wd="
    for i in range(10):
        tasks.urlopen(url + str(i))
    print("耗时：", now() - start)


if __name__ == '__main__':
    use_celery()
    # no_celery()
