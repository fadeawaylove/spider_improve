import requests
import lxml.etree
import re


class DoubanBook(object):
    tag_list_url = "https://book.douban.com/tag/?icn=index-nav"
    list_page_url = "https://book.douban.com/tag/{tag_name}?start={start}&type=T"
    book_info = ["作者", "出版社", "出品方", "原作名", "译者", "出版年", "页数", "定价", "装帧", "丛书", "ISBN", "副标题"]
    request_header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36",
        "Host": "book.douban.com",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
        "Upgrade-Insecure-Requests": "1",
        "Cookie": 'll="118282"; bid=sVgpNNcg4h0; _vwo_uuid_v2=DDF0192A91C8216C5A42BF421E30FB580|472b7c1a09d6b06a818bcbf1e7802f20; push_doumail_num=0; __utmv=30149280.20156; douban-fav-remind=1; dbcl2="201568471:ZpVhEkEQZ3I"; douban-profile-remind=1; ck=v-Tl; gr_user_id=fa3806ae-4b83-4ee8-a4ba-8a771cca6758; __utma=30149280.1614056093.1565774305.1568700472.1571111367.7; __utmc=30149280; __utmz=30149280.1571111367.7.7.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; __utma=81379588.116534101.1571111367.1571111367.1571111367.1; __utmc=81379588; __utmz=81379588.1571111367.1.1.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; __yadk_uid=8njJt3CZEiFAL75t2C1mCl02qk13t4t1; push_noty_num=0; gr_cs1_be525764-c466-4c97-a8b6-a622ee68eab1=user_id%3A1; _pk_ref.100001.3ac3=%5B%22%22%2C%22%22%2C1571138283%2C%22https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3D7u5Jw1vq1YBlhMpYoZwEx7VUVd-BW1CTtLbUtNmWiRz1ZtjdbQEQQTw_sRjP76c0%26wd%3D%26eqid%3De3985ce400063ea7000000065da541c3%22%5D; _pk_ses.100001.3ac3=*; ap_v=0,6.0; gr_session_id_22c937bbd8ebd703f2d8e9445f7dfd03=abbd1d1e-54be-497b-a155-effa705c3b21; gr_cs1_abbd1d1e-54be-497b-a155-effa705c3b21=user_id%3A1; gr_session_id_22c937bbd8ebd703f2d8e9445f7dfd03_abbd1d1e-54be-497b-a155-effa705c3b21=true; _pk_id.100001.3ac3=bffae89b4350fc30.1571111367.3.1571139703.1571128736.'
    }

    def __init__(self, offset=20):
        self.offset = offset

    def get_tags(self):
        resp = requests.get(self.tag_list_url)
        html = lxml.etree.HTML(resp.content)
        for tag in html.xpath("""//div[@class="article"]/div[2]/div"""):
            big_tag = tag.xpath("./a/@name")
            small_tag = tag.xpath("./table/tbody/tr/td/a/text()")
            print(big_tag, small_tag)
            yield big_tag, small_tag

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

    def get_book_detail(self, url):
        resp = requests.get(url, headers=self.request_header)
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
