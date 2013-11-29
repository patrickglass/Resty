"""
Metric Server Error and Exceptions
"""
import base64

class RestAuth(object):

    def __init__(self):
        self.is_authenticated = False
        self.headers = {}


class RestAuthBasic(RestAuth):

    def __init__(self, username=None, password=None):
        super(RestAuthBasic, self).__init__()
        if not username or not password:
            raise ValueError("username and password must be supplied!")
        self.userpass = base64.b64encode('%s:%s' % (username, password))
        self.headers = {
            'Authorization': 'Basic ' + self.userpass,
        }


class RestAuthToken(RestAuth):

    def __init__(self, token=None):
        super(RestAuthToken, self).__init__()
        if not token:
            raise ValueError("token must be set to a valid HTTP_Authorization token!")
        self.token = token
        self.headers = {
            'Authorization': 'Token ' + self.token,
        }
