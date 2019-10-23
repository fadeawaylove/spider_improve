# 去重方案


def get_filter_class(cls_name: str = "memory"):
    if cls_name.lower() == "bloom":
        from .bloomfilter import BloomFilter
        return BloomFilter
    elif cls_name.lower() == "memory":
        from .information_summary_filter import MemoryFilter
        return MemoryFilter
    elif cls_name.lower() == "redis":
        from .information_summary_filter import RedisFilter
        return RedisFilter
    elif cls_name.lower() == "mysql":
        from .information_summary_filter import MysqlFilter
        return MysqlFilter
    else:
        raise Exception("错误的过过滤器名 [{}]".format(cls_name))
