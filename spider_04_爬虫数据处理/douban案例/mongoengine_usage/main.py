from mongoengine import *

from models import Tag, Book
from spider import DoubanBook

spider = DoubanBook()
connect('test_db', host="192.168.219.3")

def run():
    for bt, st in spider.get_tags():
        if not Tag.objects(btag=bt[0]).all():
            for t in st:
                tag = Tag(stag=t, btag=bt[0])
                tag.save()

    for t in Tag.objects.all():  # 查询小标签出来，逐个下载
        for page, url_list in spider.get_all_list_page(t.stag):  # 获取所有翻页
            for book_url in url_list:  # 遍历列表页
                detail = spider.get_book_detail(book_url)
                detail = spider.clean_detail(detail)  # 清洗数据
                detail["small_tag"] = t.stag
                detail["big_tag"] = t.btag
                book = Book(**detail)
                book.save()
            break
        break

if __name__ == '__main__':
    run()