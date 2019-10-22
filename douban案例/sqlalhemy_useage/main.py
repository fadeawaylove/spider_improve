from models import BigTag, SmallTag, Book, BookToTag, engine
from spider import DoubanBook
from sqlalchemy.orm import sessionmaker, relationships

Session = sessionmaker(bind=engine)
spider = DoubanBook()


def store_tag_data():
    session = Session()
    for bt, st in spider.get_tags():
        current_bt = session.query(BigTag).filter_by(btag=bt[0]).first()
        if not current_bt:
            current_bt = BigTag(btag=bt[0])
            session.add(current_bt)
            session.commit()
        for t in st:
            small_tag = SmallTag(stag=t, btag_id=current_bt.id)
            session.add(small_tag)
    session.commit()
    session.close()


def store_detail_data():
    session = Session()
    for t in session.query(SmallTag).all():
        for page, url_list in spider.get_all_list_page(t.stag):
            for book_url in url_list:
                detail = spider.get_book_detail(book_url)
                detail = spider.clean_detail(detail)
                book = Book(**detail)
                print(book.title, book.author)
                exist_book = session.query(Book).filter_by(title=book.title, author=book.author).first()
                if exist_book:
                    session.delete(exist_book)
                session.add(book)
            break
        break
    session.commit()
    session.close()


if __name__ == '__main__':
    # store_tag_data()
    store_detail_data()