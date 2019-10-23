class Request(object):
    """请求对象"""

    def __init__(self, url, method="GET", query=None, body=None, name="request"):
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
        self.name = name  # 当前请求属于哪个爬虫
