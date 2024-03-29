import requests

from tornado.httpclient import HTTPClient, HTTPRequest, AsyncHTTPClient

from spidersystem.response import Response


class RequestsDownloader(object):

    def fetch(self, request):
        '''根据request发起请求，构建Response对象'''
        if request.method.upper() == "GET":
            resp = requests.get(request.url_with_query, headers=request.headers)
        elif request.method.upper() == "POST":
            resp = requests.post(request.url_with_query, headers=request.headers, body=request.body)
        else:
            raise Exception("Only support GET or POST Method!")
        return Response(request, status_code=resp.status_code, url=resp.url, headers=resp.headers, body=resp.content)


class TornadoDownloader(object):

    def __init__(self):
        self.httpclient = HTTPClient()

    def fetch(self, request):
        print("tornado 同步客户端发的请求")
        tornado_request = HTTPRequest(request.url_with_query, method=request.method.upper(), headers=request.headers)
        tornado_response = self.httpclient.fetch(tornado_request)
        return Response(request=request, status_code=tornado_response.code, url=tornado_response.effective_url,
                        headers=tornado_response.headers, body=tornado_response.buffer.read())

    def __del__(self):
        self.httpclient.close()


class AsyncTornadoDownloader(object):

    def __init__(self):
        self.async_http_client = AsyncHTTPClient()

    async def fetch(self, request):
        print("tornado 异步客户端发的请求")
        tornado_request = HTTPRequest(request.url_with_query, method=request.method.upper(), headers=request.headers)
        tornado_response = await self.async_http_client.fetch(tornado_request)
        return Response(request=request, status_code=tornado_response.code, url=tornado_response.effective_url,
                        headers=tornado_response.headers, body=tornado_response.buffer.read())


import tornado.ioloop
import asyncio
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


class ChromeHeadlessDownloader(object):

    def __init__(self, max=3):
        self.driver_pool = [self._get_driver() for i in range(max)]

    def _get_driver(self):
        driver = webdriver.Remote(command_executor="http://10.211.55.3:4444/wd/hub",
                                  desired_capabilities=DesiredCapabilities.CHROME)
        return driver

    def _fetch(self, request, driver):
        print("Use Chrome Headless")

        driver.get(request.url_with_query)

        return Response(request=request, status_code=200, url=driver.current_url, headers=driver.get_cookies(),
                        body=driver.page_source)

    async def fetch(self, request):
        while True:
            if len(self.driver_pool) >= 1:
                driver = self.driver_pool.pop(0)
                break
            await asyncio.sleep(0.5)

        io_loop = tornado.ioloop.IOLoop.current()
        response = await io_loop.run_in_executor(None, self._fetch, request, driver)
        self.driver_pool.append(driver)
        return response

    def __del__(self):
        for driver in self.driver_pool:
            driver.quit()
