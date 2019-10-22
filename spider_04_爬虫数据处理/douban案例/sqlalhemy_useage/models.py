from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Text, Float, DateTime, ForeignKey, UniqueConstraint, Index
from sqlalchemy.orm import sessionmaker, relationships
from sqlalchemy import create_engine

# engine = create_engine("mysql+pymysql://root:mysql@192.168.219.3:3306/test_db?charset=utf8", max_overflow=5)
engine = create_engine("postgresql+psycopg2://postgres:passwd@192.168.219.3:5432/test_db", max_overflow=5)

Base = declarative_base()


class BigTag(Base):
    __tablename__ = "big_tag"
    id = Column(Integer, primary_key=True, autoincrement=True)
    btag = Column(String(31), unique=True, nullable=False)
    __table_args__ = {
        "mysql_engine": "InnoDB",
        "mysql_charset": "utf8"
    }


class SmallTag(Base):
    __tablename__ = "small_tag"
    id = Column(Integer, primary_key=True, autoincrement=True)
    stag = Column(String(31), unique=True, nullable=False)
    btag_id = Column(Integer, ForeignKey("big_tag.id"))
    __table_args__ = {
        "mysql_engine": "InnoDB",
        "mysql_charset": "utf8"
    }


class Book(Base):
    __tablename__ = "book"

    author = Column(String(63), nullable=False)
    publisher = Column(String(63), nullable=False)
    producer = Column(String(63))
    original_title = Column(String(63))
    translator = Column(String(63))
    publish_time = Column(DateTime, nullable=False)
    page_number = Column(Integer)
    price = Column(Float, nullable=False)
    pack = Column(String(63))
    series = Column(String(63))
    isbn = Column(String(20), primary_key=True)
    subtitle = Column(String(63))
    title = Column(String(63), nullable=False)
    rating_num = Column(Float, nullable=False)
    book_summary = Column(Text, nullable=False)
    author_summary = Column(Text, nullable=False)

    __table_args__ = (
        UniqueConstraint('title', 'author', name='uix_title_author'),
        Index('title', 'author', 'publisher'),  # 索引
        {"mysql_engine": "InnoDB", "mysql_charset": "utf8"},  # 表的引擎
    )


# 多对多关系
class BookToTag(Base):
    __tablename__ = 'booktostag'

    id = Column(Integer, primary_key=True, autoincrement=True)
    book_isbn = Column(String(20), ForeignKey("book.isbn"))
    stag_id = Column(Integer, ForeignKey("small_tag.id"))

    __table_args__ = {
        "mysql_engine": "InnoDB",  # 表的引擎
        "mysql_charset": "utf8"  # 表的编码格式
    }


def create_all_table():
    # 创建所有表
    Base.metadata.create_all(engine)


def drop_all_table():
    # 删除所有表
    Base.metadata.drop_all(engine)


if __name__ == '__main__':
    # create_all_table()
    # drop_all_table()

    Session = sessionmaker(bind=engine)
    session = Session()
    print(session.execute("SELECT * from book;").fetchall())
