import requests

from spider_system.request import Request
from spider_system.response import Response


class Downloader(object):

    def fetch(self, request: Request):
        """根据request发起请求 构建response对象"""
        if request.method.upper() == "GET":
            resp = requests.get(request.url_with_query, headers=request.headers)
        elif request.method.upper() == "POST":
            resp = requests.post(request.url_with_query, headers=request.headers, body=request.body)
        else:
            raise Exception("不知道方法:{}!".format(request.method))
        response = Response(request, resp.status_code, resp.url, resp.headers, resp.content)
        return response
