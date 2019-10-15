import requests
import lxml.etree
import re


class DoubanBook(object):
    book_info = ["作者", "出版社", "出品方", "原作名", "译者", "出版年", "页数", "定价", "装帧", "丛书", "ISBN", "副标题"]

    def get_book_detail(self, url):
        resp = requests.get(url)
        html = lxml.etree.HTML(resp.content)
        book_info = html.xpath("""//div[@id="info"]//text()""")
        book_info_str = "".join(book_info)
        book_info_str = re.sub("\s", "", book_info_str)
        # 作者:王朔出版社:云南人民出版社出版年:2004-9页数:224定价:20.00元装帧:平装丛书:王朔文集ISBN:9787222041226
        for info in self.book_info:
            temp_info = re.search(r"({}:.*?:)".format(info), book_info_str + ":")
            if temp_info:
                temp_info = temp_info.group(0)[0: -1]
                temp_info = re.sub("{}$".format("$|".join(self.book_info)), "", temp_info)
                print(temp_info)
        book_title = html.xpath("""//div[@id="wrapper"]/h1/span/text()""")
        print(book_title)
        rating_num = html.xpath("""//div[@class="rating_self clearfix"]//strong/text()""")
        print(rating_num)
        book_summary = html.xpath("""//div[@id="link-report"]/div[1]/div[@class="intro"]/p/text()""")
        print(book_summary)
        author_summary = \
            html.xpath("""//div[@class="related_info"]/div[@class="indent "]/div/div[@class="intro"]/p/text()""")
        print(author_summary)


if __name__ == '__main__':
    douban = DoubanBook()
    douban.get_book_detail("https://book.douban.com/subject/1015584/")
