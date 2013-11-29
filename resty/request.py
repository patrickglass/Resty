"""
HTTP Requests
"""
import socket
import httplib
import urllib
import urllib2

from resty.exceptions import (
    RestApiException,
    RestApiUrlException,
    RestApiAuthError,
    RestApiBadRequest,
    RestApiServersDown
)

# def request(url, method='GET', headers={}):
#     # Perform the url request
#     try:
#         req = urllib2.Request(url, headers)
#         resp = urllib2.urlopen(req)
#         # print resp.read()
#         return resp
#     except urllib2.HTTPError as e:
#         if e.code == 403 or e.code == 401:
#             raise RestApiAuthError(e)
#         elif e.code == 400:
#             logging.error("%s: %s" % (e, e.read()))
#             raise RestApiBadRequest(e)
#         else:
#             raise RestApiUrlException(e)
#     except (urllib2.URLError, httplib.HTTPException) as e:
#         raise RestApiUrlException(e)
#     except Exception as e:
#         raise RestApiException(e)



def request(method, url, **kwargs):
    """Constructs and sends a :class:`Request <Request>`.
    Returns :class:`Response <Response>` object.

    :param method: method for the new :class:`Request` object.
    :param url: URL for the new :class:`Request` object.
    :param params: (optional) Dictionary or bytes to be sent in the query string for the :class:`Request`.
    :param data: (optional) Dictionary, bytes, or file-like object to send in the body of the :class:`Request`.
    :param headers: (optional) Dictionary of HTTP Headers to send with the :class:`Request`.
    :param cookies: (optional) Dict or CookieJar object to send with the :class:`Request`.
    :param files: (optional) Dictionary of 'name': file-like-objects (or {'name': ('filename', fileobj)}) for multipart encoding upload.
    :param timeout: (optional) Float describing the timeout of the request.
    :param allow_redirects: (optional) Boolean. Set to True if POST/PUT/DELETE redirect following is allowed.
    :param proxies: (optional) Dictionary mapping protocol to the URL of the proxy.
    :param verify: (optional) if ``True``, the SSL cert will be verified. A CA_BUNDLE path can also be provided.
    :param stream: (optional) if ``False``, the response content will be immediately downloaded.
    :param cert: (optional) if String, path to ssl client cert file (.pem). If Tuple, ('cert', 'key') pair.

    Usage::

      >>> import requests
      >>> req = requests.request('GET', 'http://httpbin.org/get')
      <Response [200]>
    """
    method = method.upper()
    if method not in ['GET', 'OPTIONS', 'HEAD',
                      'POST', 'PUT', 'PATCH', 'DELETE']:
        raise ValueError("method must be a valid HTML5 request type!")

    scheme, host, url, z1, z2 = httplib.urlsplit(url)

    headers = kwargs.get('headers', {})
    headers.setdefault('User-Agent', 'Python-Resty/1.0')
    headers.setdefault('Accept-Encoding', ', '.join(('gzip', 'deflate', 'compress')))
    headers.setdefault('Accept', '*/*')

    timeout = kwargs.get('timeout', 60)

    print url
    if scheme == "http":
        conn = httplib.HTTPConnection(host, timeout=timeout)
    elif scheme == "https":
        conn = httplib.HTTPSConnection(host, timeout=timeout)
    else:
        raise IOError("unsupported protocol: %s" % scheme)

    params = urllib.urlencode(kwargs.get('data', ''))

    # print headers, params
    conn.request(method, url, params, headers)
    resp = conn.getresponse()

    if kwargs.get('allow_redirects', False) and method in ['GET', 'OPTIONS']:
    # if method in ['GET', 'OPTIONS']:
        # We can perform a redirect if enabled and method is GET OR OPTION
        redirects = 3
        while(redirects > 0):
            if resp.status == 301:
                scheme, host, url, z1, z2 = httplib.urlsplit(url, resp.getheader('location'))
                # print url
                conn.request(method, url, params, headers)
                resp = conn.getresponse()
                redirects -= 1
            else:
                break
    conn.close()
    return resp

def _request_response(conn, method, url, params, headers):
    conn.request(method, url, params, headers)
    resp = conn.getresponse()
    return resp

def get(url, **kwargs):
    """Sends a GET request. Returns :class:`Response` object.

    :param url: URL for the new :class:`Request` object.
    :param \*\*kwargs: Optional arguments that ``request`` takes.
    """

    kwargs.setdefault('allow_redirects', True)
    return request('get', url, **kwargs)


def options(url, **kwargs):
    """Sends a OPTIONS request. Returns :class:`Response` object.

    :param url: URL for the new :class:`Request` object.
    :param \*\*kwargs: Optional arguments that ``request`` takes.
    """

    kwargs.setdefault('allow_redirects', True)
    return request('options', url, **kwargs)


def head(url, **kwargs):
    """Sends a HEAD request. Returns :class:`Response` object.

    :param url: URL for the new :class:`Request` object.
    :param \*\*kwargs: Optional arguments that ``request`` takes.
    """

    kwargs.setdefault('allow_redirects', False)
    return request('head', url, **kwargs)


def post(url, data=None, **kwargs):
    """Sends a POST request. Returns :class:`Response` object.

    :param url: URL for the new :class:`Request` object.
    :param data: (optional) Dictionary, bytes, or file-like object to send in the body of the :class:`Request`.
    :param \*\*kwargs: Optional arguments that ``request`` takes.
    """

    return request('post', url, data=data, **kwargs)


def put(url, data=None, **kwargs):
    """Sends a PUT request. Returns :class:`Response` object.

    :param url: URL for the new :class:`Request` object.
    :param data: (optional) Dictionary, bytes, or file-like object to send in the body of the :class:`Request`.
    :param \*\*kwargs: Optional arguments that ``request`` takes.
    """

    return request('put', url, data=data, **kwargs)


def patch(url, data=None, **kwargs):
    """Sends a PATCH request. Returns :class:`Response` object.

    :param url: URL for the new :class:`Request` object.
    :param data: (optional) Dictionary, bytes, or file-like object to send in the body of the :class:`Request`.
    :param \*\*kwargs: Optional arguments that ``request`` takes.
    """

    return request('patch', url,  data=data, **kwargs)


def delete(url, **kwargs):
    """Sends a DELETE request. Returns :class:`Response` object.

    :param url: URL for the new :class:`Request` object.
    :param \*\*kwargs: Optional arguments that ``request`` takes.
    """

    return request('delete', url, **kwargs)
