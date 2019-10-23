class Response(object):

    def __init__(self, request, status_code, url, headers, body):
        self.request = request
        self.status_code = status_code
        self.url = url
        self.headers = headers
        self.body = body
