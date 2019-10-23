from . import BaseFilter
import pymysql as MySQLdb
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


# class Filter(Base):
#     __tablename__ == "filter"
#     id = Column(Integer, primary_key=True)
#     hash_value = Column(String(40), index=True, unique=True)


class MysqlFilter(BaseFilter):

    def __init__(self, *args, **kwargs):
        self.mysql_host = kwargs.get("mysql_host") or "localhost"
        self.mysql_port = kwargs.get("mysql_port") or 3306
        self.mysql_user = kwargs.get("mysql_user") or "root"
        self.mysql_password = kwargs.get("mysql_password")
        self.mysql_db = kwargs.get("mysql_db")
        self.mysql_table = kwargs.get("mysql_table")
        self.mysql_url = f"mysql+pymysql://{self.mysql_user}:{self.mysql_password}@{self.mysql_host}:{self.mysql_port}/{self.mysql_db}?charset=utf8"
        self.table = type(
            self.mysql_table,
            (Base,),
            dict(
                __tablename__=self.mysql_table,
                id=Column(Integer, primary_key=True),
                hash_value=Column(String(40), index=True, unique=True)
            )
        )
        super(MysqlFilter, self).__init__(*args, **kwargs)

    def _save(self, hash_value):
        session = self.storage()
        f = self.table(hash_value=hash_value)
        session.add(f)
        session.commit()
        session.close()

    def _is_exists(self, hash_value):
        session = self.storage()
        ret = session.query(self.table).filter_by(hash_value=hash_value).first()
        session.close()
        return True if ret else False

    def _get_storage(self):
        engine = create_engine(self.mysql_url)
        Base.metadata.create_all(engine)
        Session = sessionmaker(engine)
        return Session
