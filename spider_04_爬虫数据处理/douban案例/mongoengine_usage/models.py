from mongoengine import *


class Tag(Document):
    stag = StringField(required=True, max_length=31)
    btag = StringField(required=True, max_length=31)

class Book(Document):
    '''
    {
      "author": str,
      "publisher": str,
      "producer": str,
      "original_title": str,
      "translator": str,
      "publish_time": datetime,
      "page_number": int,
      "price": float,
      "pack": str,
      "series": str,
      "isbn": str/long int,
      "subtitle": str,
      "title": str,
      "rating_num": float,
      "book_summary": text,
      "author_summary": text
    }
    '''

    author = StringField(required=True, max_length=63)
    publisher = StringField(required=True, max_length=63)
    producer = StringField(max_length=63)
    original_title = StringField(max_length=63)
    translator = StringField(max_length=63)
    publish_time = DateTimeField(required=True)
    page_number = IntField(required=True)
    price = FloatField(required=True)
    pack = StringField(max_length=63)
    series = StringField(max_length=63)
    isbn = StringField(required=True, max_length=63)
    subtitle = StringField(max_length=63)
    title = StringField(required=True, max_length=63)
    rating_num = FloatField(required=True)
    book_summary = StringField(required=True)
    author_summary = StringField(required=True)

    # 因为是nosql，如果这些数据采取冗余的方式存储
    small_tag = StringField(required=True, max_length=31)
    big_tag = StringField(required=True, max_length=31)
