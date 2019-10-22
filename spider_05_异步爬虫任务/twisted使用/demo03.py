from twisted.internet import reactor
from twisted.web.client import Agent
from twisted.web.http_headers import Headers

'''创建一个数据生产者，实现POST请求'''
from zope.interface import implementer
from twisted.internet.defer import succeed
from twisted.web.iweb import IBodyProducer


@implementer(IBodyProducer)
class BytesProducer(object):
    def __init__(self, body):
        self.body = body
        self.length = len(body)

    def startProducing(self, consumer):
        consumer.write(self.body)
        return succeed(None)

    def pauseProducing(self):
        pass

    def stopProducing(self):
        pass


# 创建agent对象
agent = Agent(reactor)

# agent.request返回一个defered对象，用于设置回调函数
defered = agent.request(
    b'POST',
    b'http://www.baidu.com/s?wd=python',  # 该接口此处无效，它只处理get请求
    Headers({'User-Agent': ['Twisted Web Client Example']}),
    BytesProducer('请求体'.encode())  # 利用BytesProducer转换数据
)


def successCallback(response):
    print('Response received：', response)


# 设置成功回调：如果任务执行成功，那么将会调用该回调函数
defered.addCallback(successCallback)


def errorCallback(error):
    print("errback: ", str(error))


# 设置失败回调：如果任务执行中出现异常或成功回调函数出现异常，那么将会调用失败回调
defered.addErrback(errorCallback)


def callbackShutdown(ignored):
    reactor.stop()


# 设置最终回调：无论成功和失败，都必然会调用的回调函数
defered.addBoth(callbackShutdown)

# addCallback/addErrback/addBoth的逻辑类似于try/except/finally

# 启动事件循环
reactor.run()
