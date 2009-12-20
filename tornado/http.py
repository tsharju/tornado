import calendar
import email.utils


class HTTPRequest(object):
    def __init__(self, url, method="GET", headers={}, body=None,
                 auth_username=None, auth_password=None,
                 connect_timeout=None, request_timeout=None,
                 if_modified_since=None, follow_redirects=True,
                 max_redirects=5, user_agent=None, use_gzip=True,
                 network_interface=None, streaming_callback=None):
        if if_modified_since:
            timestamp = calendar.timegm(if_modified_since.utctimetuple())
            headers["If-Modified-Since"] = email.utils.formatdate(
                timestamp, localtime=False, usegmt=True)
        if "Pragma" not in headers:
            headers["Pragma"] = ""
        self.url = _utf8(url)
        self.method = method
        self.headers = headers
        self.body = body
        self.auth_username = _utf8(auth_username)
        self.auth_password = _utf8(auth_password)
        self.connect_timeout = connect_timeout or 20.0
        self.request_timeout = request_timeout or 20.0
        self.follow_redirects = follow_redirects
        self.max_redirects = max_redirects
        self.user_agent = user_agent
        self.use_gzip = use_gzip
        self.network_interface = network_interface
        self.streaming_callback = streaming_callback


class HTTPResponse(object):
    def __init__(self, request, code, headers={}, body="", effective_url=None,
                 error=None, request_time=None):
        self.request = request
        self.code = code
        self.headers = headers
        self.body = body
        if effective_url is None:
            self.effective_url = request.url
        else:
            self.effective_url = effective_url
        if error is None:
            if self.code < 200 or self.code >= 300:
                self.error = HTTPError(self.code)
            else:
                self.error = None
        else:
            self.error = error
        self.request_time = request_time

    def rethrow(self):
        if self.error:
            raise self.error

    def __repr__(self):
        args = ",".join("%s=%r" % i for i in self.__dict__.iteritems())
        return "%s(%s)" % (self.__class__.__name__, args)


class HTTPError(Exception):
    def __init__(self, code, message=None):
        self.code = code
        message = message or httplib.responses.get(code, "Unknown")
        Exception.__init__(self, "HTTP %d: %s" % (self.code, message))


def _utf8(value):
    if value is None:
        return value
    if isinstance(value, unicode):
        return value.encode("utf-8")
    assert isinstance(value, str)
    return value
