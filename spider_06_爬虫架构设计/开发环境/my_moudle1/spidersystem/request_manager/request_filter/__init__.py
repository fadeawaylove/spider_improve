# 实现请求去重的逻辑
import urllib.parse


class RequestFilter(object):

    def __init__(self, filter_obj):
        self.filter_obj = filter_obj

    def is_exists(self, request_obj):
        '''
        判断请求是够已经处理过
        return: True or False
        '''
        data = self._get_request_filter_data(request_obj)
        return self.filter_obj.is_exists(data)

    def mark_request(self, request_obj):
        '''
        标记已经处理过的请求对象
        :param request_obj:
        :return: 标记
        '''
        data = self._get_request_filter_data(request_obj)
        return self.filter_obj.save(data)

    def _get_request_filter_data(self, request_obj):
        '''
        根据一个请求对象，处理他的...  转换为字符串  然后再进行去重处理
        :param request_obj:
        :return: 转换后的字符串
        '''
        # 1.URL:  HTTPS://WWW.BAIDU.com/S   ?wd=PYTHON&a=100&b=200
        #         HTTPS://WWW.BAIDU.com/S?wd=PYTHON&b=200&a=100
        #         HTTPS://WWW.BAIDU.com/S?a=100&b=200&wd=PYTHON
        # 把协议和域名部分进行大小写统一，其他的保留原始大小写格式
        # 对查询参数进行简单的排序，然后和后面query进行合并
        url = request_obj.url
        _ = urllib.parse.urlparse(url)
        url_without_query = _.scheme + "://" + _.hostname + _.path
        url_query = urllib.parse.parse_qsl(_.query)

        # 2.method: "Get".upper()
        method = request_obj.method.upper()

        # 3.query: str(sorted({}.items()))  [()]   str([])
        # {"c":100}
        # 考虑：把url中的请求查询参数和query里的进行合并
        query = request_obj.query.items()
        all_query = sorted(set(list(query) + url_query))
        # print(all_query)

        url_with_query = url_without_query + "?" + urllib.parse.urlencode(all_query)

        # 4.body: str(sorted({}.items()))
        str_body = str(sorted(request_obj.body.items()))

        data = url_with_query + method + str_body
        # url  method  body

        return data

