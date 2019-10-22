from twisted.internet import reactor
from twisted.internet.defer import Deferred, DeferredList
from twisted.internet.protocol import Protocol
from twisted.web.client import Agent
from twisted.web.http_headers import Headers


# 创建一个协议Protocol类，用来收集数据
class BodyCollector(Protocol):
    def __init__(self, finished, uri):
        self.finished = finished  # 外部定义的defered对象，用于数据接收完毕后，触发相应回调函数
        self.uri = uri
        self.body = bytes()

    def dataReceived(self, data):
        '''每接收到一次数据，该方法就会被调用一次'''
        print("data_uri: ", self.uri, data)
        self.body += data  # 收集所有的的响应数据

    def connectionLost(self, reason):
        '''当socket连接关闭后，该方法会被调用'''
        print('已完成数据的收集:', reason.getErrorMessage())
        # 触发对应的回调函数
        self.finished.callback(self.body)


agent = Agent(reactor)


def successCallback(response):
    '''此时还没有开始响应体，但已经收到响应头的信息，如下：'''
    # print('Response version:', response.version)
    # print('Response code:', response.code)
    # print('Response phrase:', response.phrase)
    # print('Response headers:')
    # print(pformat(list(response.headers.getAllRawHeaders())))
    finished = Deferred()
    # deliverBody方法接收一个Protocol对象，用来异步地接收数据
    response.deliverBody(BodyCollector(finished, response.request.absoluteURI))

    def handleBody(body):
        print("twisted: ", len(body))

    finished.addCallback(handleBody)  # 当完成后，回调会在Protocol类中调用

    def errorCallback(error):
        print(response.request.absoluteURI, error)

    finished.addErrback(errorCallback)
    return finished


_ = []
for url in [
    b"http://www.baidu.com",
    b"https://www.taobao.com",
    b"https://www.jd.com",
    b"https://www.tmall.com",
    b"https://www.tencent.com",
    b"https://www.douban.com", ]:
    d = agent.request(
        b'GET',
        url,
        Headers({'User-Agent': ['Twisted Web Client Example']}),
        None)
    d.addCallback(successCallback)
    _.append(d)

dl = DeferredList(_)  # 统一管理多个defered对象


def callbackShutdown(ignored):
    reactor.stop()


dl.addBoth(callbackShutdown)

if __name__ == '__main__':
    reactor.run()
