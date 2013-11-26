import socket
import httplib
import urllib2

def request(url, headers=''):
    # Perform the url request
    try:
        req = urllib2.Request(url, str(headers))
        resp = urllib2.urlopen(req)
        # print resp.read()
        return resp
    except urllib2.HTTPError as e:
        if e.code == 403 or e.code == 401:
            raise RestApiAuthError(e)
        elif e.code == 400:
            logging.error("%s: %s" % (e, e.read()))
            raise RestApiBadRequest(e)
        else:
            raise RestApiUrlException(e)
    except (urllib2.URLError, httplib.HTTPException) as e:
        raise RestApiUrlException(e)
    except Exception as e:
        raise RestApiException(e)
