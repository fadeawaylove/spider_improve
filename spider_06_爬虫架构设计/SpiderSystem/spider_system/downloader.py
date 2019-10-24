import requests
import json

from spider_system.request import Request
from spider_system.response import Response
from tornado.httpclient import HTTPClient, HTTPRequest, AsyncHTTPClient


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


class TornadoDownloader(object):

    def __init__(self):
        self.http_client = HTTPClient()

    def fetch(self, request: Request):
        tornado_request = HTTPRequest(
            url=request.url_with_query,
            method=request.method.upper(),
            headers=request.headers) if request.method.upper() == "GET" else \
            HTTPRequest(
                url=request.url_with_query,
                method=request.method.upper(),
                headers=request.headers, body=json.dumps(request.body))
        tornado_reponse = self.http_client.fetch(tornado_request)
        return Response(request=request, status_code=tornado_reponse.code, url=tornado_reponse.effective_url,
                        headers=tornado_reponse.headers, body=tornado_reponse.body)

    def __del__(self):
        self.http_client.close()


class TornadoAsyncDownloader(object):

    def __init__(self):
        self.http_client = AsyncHTTPClient()

    async def fetch(self, request: Request):
        tornado_request = HTTPRequest(
            url=request.url_with_query,
            method=request.method.upper(),
            headers=request.headers) if request.method.upper() == "GET" else \
            HTTPRequest(
                url=request.url_with_query,
                method=request.method.upper(),
                headers=request.headers, body=json.dumps(request.body))
        tornado_reponse = await self.http_client.fetch(tornado_request)
        return Response(request=request, status_code=tornado_reponse.code, url=tornado_reponse.effective_url,
                        headers=tornado_reponse.headers, body=tornado_reponse.body)
