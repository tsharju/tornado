from tornado.http import HTTPRequest, HTTPError, HTTPResponse

from google.appengine.api import urlfetch


class HTTPClient(object):

    def __init__(self, max_simultaneous_connections=None):
        pass

    def fetch(self, request, callback=None, **kwargs):
        if not isinstance(request, HTTPRequest):
            request = HTTPRequest(url=request, **kwargs)
        url = request.url
        payload = request.body
        method = request.method
        headers = request.headers
        follow_redirects = request.follow_redirects
        deadline = request.connect_timeout or request.request_timeout or 20
        allow_truncated = True
        result = urlfetch.fetch(url, payload, method, headers,
                                allow_truncated, follow_redirects, deadline)
        if result.status_code < 200 or result.status_code >= 300:
            raise HTTPError(result.status_code)
        response = HTTPResponse(
            request=request, code=result.status_code, headers=result.headers,
            body=result.content, effective_url=result.final_url)
        if callback:
            return callback(response)
        else:
            return response
