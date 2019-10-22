from tornado import httpclient, ioloop


async def spider():
    http_client = httpclient.AsyncHTTPClient()
    try:
        # fetch返回的是一个future对象
        response = await http_client.fetch("http://www.baidu.com")
    except Exception as e:
        print("Error: %s" % e)
    else:
        print(response.effective_url)
        print(response.body)


if __name__ == '__main__':
    # 获取当前线程的事件循环，类似asyncio.get_event_loop
    io_loop = ioloop.IOLoop.current()
    # 运行spider协程，直到运行完毕后就退出循环，类似asyncio_loop.run_until_complete
    io_loop.run_sync(spider)
