import requests
import lxml.etree


class DoubanBook(object):
    tag_list_url = "https://book.douban.com/tag/?icn=index-nav"

    def get_tags(self):
        resp = requests.get(self.tag_list_url)
        html = lxml.etree.HTML(resp.content)
        for tag in html.xpath("""//*[@id="content"]/div/div[1]/div[2]/div"""):
            big_tag = tag.xpath("./a/@name")
            small_tag = tag.xpath("./table/tbody/tr/td/a/text()")
            print(big_tag)
            print(small_tag)


if __name__ == '__main__':
    douban_book = DoubanBook()
    douban_book.get_tags()
