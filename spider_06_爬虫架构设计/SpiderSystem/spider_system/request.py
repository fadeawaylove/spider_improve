import urllib.parse


class Request(object):
    """请求对象"""

    def __init__(self, url, method="GET", query=None, body=None, name="request", headers=None, id =None):
        self.url = url
        self.method = method
        if query is None:
            query = {}
        if body is None:
            body = {}
        if not isinstance(query, dict):
            raise Exception("query must be dict type")
        self.query = query
        if not isinstance(body, dict):
            raise Exception("body must be dict type")
        self.body = body
        self.headers = headers

        self.name = name  # 当前请求属于哪个爬虫

        self.id = id  # fp指纹

    @property
    def url_with_query(self):

        url_object = urllib.parse.urlparse(self.url)
        url_path = url_object.scheme + "://" + url_object.hostname + url_object.path
        url_query = urllib.parse.parse_qsl(url_object.query)
        query = sorted(set(list(self.query.items()) + url_query))
        return url_path + "?" + urllib.parse.urlencode(query)


if __name__ == '__main__':
    r = Request("http://www.baidu.com/s?wd=123", query={"a": 1, "wd": "123", "b": 1})
    print(r.url_with_query)
