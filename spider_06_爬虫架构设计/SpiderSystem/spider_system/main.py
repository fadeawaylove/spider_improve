from spider_system.request import Request
from spider_system.request_manager import RequestScheduler
from spider_system.request_manager.utils.redis_tools import get_redis_queue_cls
from spider_system.downloader import Downloader

FILTER_QUEUE = get_redis_queue_cls("fifo")


class Master(object):

    def __init__(self, spiders, request_manager_config, project_name):
        self.filter_queue = FILTER_QUEUE("filter_queue", host="192.168.219.3")  # 请求去重队列，等待过滤的原始请求
        self.request_manager = RequestScheduler(**request_manager_config)  # 包含去重过滤器和存储请求的队列（优先级，fifo，lifo）
        self.spiders = spiders
        self.project_name = project_name

    def run_start_request(self):
        for spider in self.spiders.values():
            for request in spider().start_requests():
                self.filter_queue.put(request)

    def run_filter_queue(self):
        while True:
            request = self.filter_queue.get()
            self.request_manager.add_request(request, self.project_name)

    def run(self):
        self.run_start_request()
        self.run_filter_queue()


class Slave(object):

    def __init__(self, spiders, request_manager_config, project_name):
        self.filter_queue = FILTER_QUEUE("filter_queue", host="192.168.219.3")  # 请求去重队列，等待过滤的原始请求
        self.request_manager = RequestScheduler(**request_manager_config)  # 包含去重过滤器和存储请求的队列（优先级，fifo，lifo）
        self.downloader = Downloader()
        self.spiders = spiders
        self.project_name = project_name

    def run(self):
        while True:
            request = self.request_manager.get_request(self.project_name)
            resp = self.downloader.fetch(request)
            spider = self.spiders[request.name]()

            for result in spider.parse(resp):
                if result is None:
                    raise Exception("不允许返回None！")
                if isinstance(result, Request):
                    self.filter_queue.put(result)
                else:
                    new_result = spider.data_clean(result)
                    spider.data_save(new_result)
