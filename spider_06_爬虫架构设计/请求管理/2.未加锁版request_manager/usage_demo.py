from six.moves import queue

from request_manager.request import Request
from request_manager import RequestScheduler

REQUEST_SCHEDULER_CONFIG = {
    "queue_type": "fifo",
    # 如何配置需查看redis队列的实例化时需要的参数  redis_queue模块中
    # 注意：redis的key会被queue_name重写，因此此处不用写
    "queue_kwargs": {"host": "192.168.219.3", "port": 6379, "db": 2},

    "filter_type": "redis",
    # 如何配置需查看对应过滤器实例化时如何传参   filter_class模块中
    # 注意：redis的key或mysql的表名称 会被filter_name重写，因此此处不用写
    "filter_kwargs": {"redis_key": "redis_filter", "redis_host": "192.168.219.3"},
}

request_scheduler = RequestScheduler(**REQUEST_SCHEDULER_CONFIG)

baidu_url = "https://www.baidu.com/s?wd="
taobao_url = "https://www.taobao.com?sid="

request_objs = [
    Request(baidu_url + "1", name="baidu"),
    Request(baidu_url + "1", name="baidu"),
    Request(baidu_url + "2", name="baidu"),
    Request(baidu_url + "3", name="baidu"),

    Request(taobao_url + "a", name="taobao"),
    Request(taobao_url + "b", name="taobao"),
    Request(taobao_url + "c", name="taobao"),
    Request(taobao_url + "c", name="taobao"),
]


def add_requests(objs):
    # 添加请求
    for r in objs:
        request_scheduler.add_request(r, r.name)


def get_requests(queue_name):
    # 获取请求
    while True:
        try:
            request = request_scheduler.get_request(queue_name, block=False)
        except queue.Empty:
            break
        else:
            yield request


add_requests(request_objs)

for request in get_requests("baidu"):
    print(request.url)

for request in get_requests("taobao"):
    print(request.url)
