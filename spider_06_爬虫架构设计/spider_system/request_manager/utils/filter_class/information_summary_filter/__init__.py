# 基于信息摘要算法进行数据的去重判断和存储

# 1.基于内存
# 2.基于redis
# 3.基于mysql
import six
import hashlib


class BaseFilter(object):

    def __init__(self, hash_func_name="md5", *args, **kwargs):
        self.hash_func = getattr(hashlib, hash_func_name)
        self.storage = self._get_storage()

    @staticmethod
    def _safe_data(data):
        """
        将data预处理为可以进行hash处理的类型
        :param data:
        :return:
        """
        if six.PY3:
            if isinstance(data, str):
                return data.encode()
            elif isinstance(data, bytes):
                return data
            else:
                raise Exception("请提供一个字符串或者二进制")
        else:
            if isinstance(data, str):
                return data
            elif isinstance(data, unicode):
                return data.encode()
            else:
                raise Exception("请提供一个字符串或者unicode")

    def _get_hash_value(self, data):
        """
        获取data的hash值
        :param data: python3:bytes python2:str
        :return:
        """
        hash_obj = self.hash_func()
        hash_obj.update(self._safe_data(data))
        return hash_obj.hexdigest()

    def _get_storage(self):
        """
        返回一个存储对象
        :return:
        """
        pass

    def _save(self, hash_value):
        """
        实际的存储指纹的方法
        :param hash_value:
        :return:
        """

    def _is_exists(self, hash_value):
        """
        实际的判断是否存在的方法
        :param hash_value:
        :return:
        """

    def save(self, data):
        """
        根据data计算出对用的指纹进行存储
        :param data: 给定的原始数据
        :return: 返回存储结果
        """
        hash_value = self._get_hash_value(data)
        return self._save(hash_value)

    def is_exists(self, data):
        """
        判断给定数据的指纹是否存在
        :param data:
        :return: True or False
        """
        return self._is_exists(self._get_hash_value(data))


from .mysql_filter import MysqlFilter
from .redis_filter import RedisFilter
from .memory_filter import MemoryFilter
