"""
This class implements a simple rest api framework for interfacing with the
Server via its REST API.
"""
import json

from resty.exceptions import (
    RestApiException,
    RestApiUrlException,
    RestApiAuthError,
    RestApiBadRequest,
    RestApiServersDown
)
from resty.resource import RestResource
from resty.auth import RestAuth, RestAuthToken
from resty.request import request

class RestyAPI(object):
    """
    Used to easily consume a django-rest-framework compatable API.
    it can discover all the resources automatically and imports the field
    validation.
    """

    def __init__(self, baseUrl='', token=None):
        self.resources = {}
        self.url = None
        self.auth = None
        if baseUrl:
            self.url = baseUrl
        if token:
            self.auth = RestAuthToken(token)
        self.headers = {
            'Content-Type': 'application/json'
        }

    @property
    def url(self):
        return self._url

    @url.setter
    def url(self, value):
        if isinstance(value, basestring):
            self._url = value.strip('/') + '/'
        elif value is None:
            self._url = value
        else:
            raise ValueError("url should be a string representing a URL")
        return self._url

    @property
    def auth(self):
        return self._auth

    @auth.setter
    def auth(self, value):
        if value is not None and not isinstance(value, RestAuth):
            raise ValueError("auth must be derrived from RestAuth class!")
        self._auth = value
        return self._auth

    def resource(self, name):
        """
        Creates an object to consume a resource on a remote REST API
        eg. api.resource(name).one(id)
            will GET on /{name}/{id}/
        """
        if name in self.resources:
            res = self.resources[name]
        else:
            url = self.url + '/' + name.strip('/') + '/'
            res = RestResource(url)
            self.resources[name] = res
        return res

    def list_resources(self):
        return self.resources.keys()

    def discover(self):
        """
        Will use the baseURL and query the remote server to auto determine
        the resources and the field validation for each resource
        """
        # Get the global headers and set any extra headers
        headers = self.headers.copy()
        headers.update(self.auth.headers)

        data = request('GET', self.url, headers=headers).read()
        resources = json.loads(data)
        for res in resources:
            self.resource(res)


