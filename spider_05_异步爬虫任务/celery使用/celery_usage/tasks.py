from __future__ import absolute_import, print_function, unicode_literals
import requests
from celery import Celery

app = Celery()
app.config_from_object("celeryconfig")


# 使用task装饰器，注册urlopen函数为task
# ignore_result如果为True，意味着celery不会存储函数的返回结果
@app.task(ignore_result=False)
def urlopen(url):
    print('Opening: {0}'.format(url))
    try:
        response = requests.get(url)
    except requests.exceptions.RequestException as exc:
        print('Exception for {0}: {1!r}'.format(url, exc))
        return "fail", url
    print('Done with: {0}'.format(url))
    # 返回的结果必须是能被json序列化的数据
    # 如unicode类型字符串、数值、含有unicode类型字符串或数值的字典、列表等
    return {"url": url}


if __name__ == '__main__':
    pass
