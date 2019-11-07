# 基于mysql的去重判断依据的存储

from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from . import BaseFilter

Base = declarative_base()


class MySQLFilter(BaseFilter):
    '''基于mysql的去重判断依据的存储'''

    def __init__(self, *args, **kwargs):

        # 动态创建基于Base的类，从而实现动态创建表，
        table = type(
            kwargs["mysql_table_name"],
            (Base,),
            dict(
                __tablename__ = kwargs["mysql_table_name"],
                id=Column(Integer, primary_key=True),
                hash_value=Column(String(40), index=True, unique=True)
            ))

        self.table = table

        BaseFilter.__init__(self, *args, **kwargs)

    def _get_storage(self):
        '''返回一个mysql连接对象(sqlalchemy的数据库连接对象)'''
        engine = create_engine(self.mysql_url)
        Base.metadata.create_all(engine)   # 创建表、如果有就忽略
        Session = sessionmaker(engine)
        return Session

    def _save(self, hash_value):
        '''
        利用redis的无序集合进行存储
        :param hash_value:
        :return:
        '''
        session = self.storage()
        filter = self.table(hash_value=hash_value)
        session.add(filter)
        session.commit()
        session.close()

    def _is_exists(self, hash_value):
        '''判断redis对应的无序集合中是否有对应的判断依据'''
        session = self.storage()
        ret = session.query(self.table).filter_by(hash_value=hash_value).first()
        session.close()
        if ret is None:
            return False
        return True






