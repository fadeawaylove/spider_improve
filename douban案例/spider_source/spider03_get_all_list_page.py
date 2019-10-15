import requests
import lxml.etree


class DoubanBook(object):
    list_page_url = "https://book.douban.com/tag/{tag_name}?start={start}&type=T"

    def __init__(self, offset=20):
        self.offset = offset

    def get_list_page(self, tag_name, page_num):
        """获取详情页地址"""
        resp = requests.get(self.list_page_url.format(tag_name=tag_name, start=(page_num - 1) * self.offset))
        html = lxml.etree.HTML(resp.content)
        detail_page_url_list = html.xpath("""//*[@id="subject_list"]/ul/li/div[1]/a/@href""")
        has_next = True if html.xpath("""//span[@class="next"]/a/@href""") else False
        # print(has_next, detail_page_url_list)
        # print(has_next, resp.url)
        return has_next, detail_page_url_list

    def get_all_list_page(self, tag_name, page_num=0):
        """获取所有详情页的地址"""
        hash_next, url_list = self.get_list_page(tag_name, page_num)
        yield page_num, url_list
        if hash_next:
            yield from self.get_all_list_page(tag_name, page_num + 1)


if __name__ == '__main__':
    douban = DoubanBook()
    # douban.get_list_page("小说", 2)
    for page in douban.get_all_list_page("小说"):
        print(page)
