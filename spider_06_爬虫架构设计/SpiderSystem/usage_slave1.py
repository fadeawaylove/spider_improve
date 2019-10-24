import tornado.ioloop

from spider_system.main import Master, Slave

from spider_system.spider import BaseSpider
from spider_system.request import Request
from spider_system.response import Response

REQUEST_MANAGER_CONFIG = {
    # 请求队列设置，去重后的请求都存在这里面
    "queue_type": "fifo",
    "queue_kwargs": {"host": "192.168.219.3", "port": 6379, "db": 2},

    # 过滤器的配置，使用的是redis过滤器
    "filter_type": "redis",
    "filter_kwargs": {"redis_key": "redis_filter", "redis_host": "192.168.219.3"},
}
PROJECT_NAME = "baidu"


class BaiduSpider(BaseSpider):
    name = "baidu"

    def start_requests(self):
        yield Request("http://www.baidu.com", name=self.name)
        yield Request("http://www.baidu.com/s?wd=python2", name=self.name)
        yield Request("http://www.baidu.com/s?wd=python3", name=self.name)
        yield Request("http://www.baidu.com/s?wd=python4", name=self.name)

    def parse(self, response: Response):
        """生成器，返回有两种，Request或者data"""
        # print(response)
        print(response.url)
        # print(response.body)
        yield response.body

    def data_clean(self, data):
        return data

    def data_save(self, data):
        pass


if __name__ == '__main__':
    spiders = {BaiduSpider.name: BaiduSpider}
    # Slave(spiders, request_manager_config=REQUEST_MANAGER_CONFIG, project_name=PROJECT_NAME).run()
    io_loop = tornado.ioloop.IOLoop.current()
    io_loop.run_sync(Slave(spiders, request_manager_config=REQUEST_MANAGER_CONFIG, project_name=PROJECT_NAME).run)
