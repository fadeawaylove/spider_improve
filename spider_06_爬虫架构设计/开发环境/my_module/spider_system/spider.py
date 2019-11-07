from spider_system.response import Response
from spider_system.request import Request


class BaseSpider(object):
    name = "demo"

    def start_requests(self):
        yield Request("http://www.baidu.com/s?wd=python", name=self.name)

    def parse(self, response: Response):
        """生成器，返回有两种，Request或者data"""
        yield

    def data_clean(self, data):
        return data

    def data_save(self, data):
        pass
