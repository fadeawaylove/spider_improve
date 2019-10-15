import lxml.etree

import requests


class DoubanBook(object):
    list_page_url = "https://book.douban.com/tag/{tag_name}?start={start}&type=T"

    def get_list_page(self, tag_name, page_num):
        """获取详情页地址"""
        offset = 20
        resp = requests.get(self.list_page_url.format(tag_name=tag_name, start=(page_num - 1) * offset))
        html = lxml.etree.HTML(resp.content)
        detail_page_url_list = html.xpath("""//*[@id="subject_list"]/ul/li/div[1]/a/@href""")
        print(detail_page_url_list)


if __name__ == '__main__':
    douban = DoubanBook()
    douban.get_list_page("小说", 2)
