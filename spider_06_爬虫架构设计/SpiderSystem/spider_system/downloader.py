import requests
import json

import asyncio
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


import time
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


class ChromeDownloader(object):
    def __init__(self, max=3):
        self.driver_pool = [self._get_driver() for _ in range(max)]
        print(self.driver_pool)

    def _get_driver(self):
        return webdriver.Remote("http://192.168.219.3:4444/wd/hub", desired_capabilities=DesiredCapabilities.CHROME)

    async def fetch(self, request):
        print("chrome 开始发送请求了：{}".format(request.url_with_query))

        while True:
            if self.driver_pool:
                driver = self.driver_pool.pop(0)
                break
            await asyncio.sleep(0.5)

        loop = asyncio.get_event_loop()
        await loop.run_in_executor(driver.get, request.url_with_query)

        resp = Response(body=driver.page_source, request=request, url=driver.current_url,
                        headers=driver.get_cookies(), status_code=200)
        self.driver_pool.append(driver)
        return resp

    def __del__(self):
        for driver in self.driver_pool:
            driver.quit()
