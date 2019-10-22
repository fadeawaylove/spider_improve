from gevent.pool import Pool
import urllib.request

# 打补丁
import gevent.monkey

gevent.monkey.patch_all()


def spider(url):
    print("Coroutine(%s): spider[%s] start" % (gevent.getcurrent().name, url))
    urllib.request.urlopen(url, timeout=2)
    print("Coroutine(%s): spider[%s] done" % (gevent.getcurrent().name, url))


if __name__ == '__main__':
    urls = [
        "https://www.baidu.com",
        "https://www.google.com",  # 该请求
        "http://www.jd.com",
        "http://www.taobao.com",
        "https://www.tencent.com"
    ]

    pool = Pool(3)
    for url in urls:
        pool.apply_async(spider, args=(url,))
    pool.join()

    '''运行结果：
    Coroutine(Greenlet-0): spider[https://www.baidu.com] start
    Coroutine(Greenlet-1): spider[https://www.google.com] start
    Coroutine(Greenlet-2): spider[http://www.jd.com] start
    Coroutine(Greenlet-2): spider[http://www.jd.com] done
    Coroutine(Greenlet-2): spider[http://www.taobao.com] start
    Coroutine(Greenlet-0): spider[https://www.baidu.com] done
    Coroutine(Greenlet-0): spider[https://www.tencent.com] start
    Coroutine(Greenlet-0): spider[https://www.tencent.com] done
    Coroutine(Greenlet-2): spider[http://www.taobao.com] done
    ...异常信息
    '''

    '''分析
    由于google.com不搭建梯子无法访问，同时由于设置了timeout
    所以导致请求google.com的1号greenlet，出现异常而退出了

    这些特征都非常类似多线程或多进程，可以看出gevent的程序设计风格，非常符合利用多线程、多进程的设计风格
    '''
