from spider_system.main import Master, Slave

from spider_system.spider import BaseSpider
from spider_system.request import Request
from spider_system.response import Response


class BaiduSpider(BaseSpider):
    name = "baidu"

    def start_requests(self):
        yield Request("http://www.baidu.com", name=self.name)

    def parse(self, response: Response):
        """生成器，返回有两种，Request或者data"""
        print(response)
        print(response.url)
        print(response.body)
        yield response.body

    def data_clean(self, data):
        return data

    def data_save(self, data):
        pass


if __name__ == '__main__':
    spiders = {BaiduSpider.name: BaiduSpider}
    Master(spiders).run()
    Slave(spiders).run()
