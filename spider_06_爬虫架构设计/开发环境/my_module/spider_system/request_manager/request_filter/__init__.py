import urllib.parse


class RequestFilter(object):

    def __init__(self, filter_obj):
        self.filter = filter_obj

    def mark_request(self, request_obj):
        data = self._get_request_filter_data(request_obj)
        return self.filter.save(data)

    def is_exists(self, request_obj):
        return self.filter.is_exists(self._get_request_filter_data(request_obj))

    def _get_request_filter_data(self, request_obj):
        """
        根据一个请求对象，处理他的...  转换为字符串  然后再进行去重处理
        :param request_obj:
        :return:
        """

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

        url_with_query = url_without_query + "?" + urllib.parse.urlencode(all_query)

        # 4.body: str(sorted({}.items()))
        str_body = str(sorted(request_obj.body.items()))

        data = url_with_query + method + str_body
        # url  method  body
        return data
