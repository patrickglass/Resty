#!/usr/bin/env python
"""
UnitTest framework for validating the Resty system
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "../"))
import time
from unittest import TestCase, main
from mock import patch
import random
import urllib2
import json
from StringIO import StringIO

from resty.api import RestyAPI, RestApiException, RestApiAuthError
from resty.auth import RestAuth, RestAuthBasic, RestAuthToken
from resty.request import request


REST_HOST = 'localhost:8080'
REST_URL = 'http://' + REST_HOST + '/api/v1/'
REST_AUTH_TOKEN = 'AUTH_TOKEN_GOES_HERE'


class TestRestyInit(TestCase):

    def test_no_args(self):
        self.assertTrue(RestyAPI())

    def test_url(self):
        api = RestyAPI()
        url = object()
        self.assertRaises(ValueError, setattr, api, 'url', url)

    def test_bad_authclass(self):
        api = RestyAPI()
        auth = object()
        self.assertRaises(ValueError, setattr, api, 'auth', auth)

    def test_ok_authclass(self):
        api = RestyAPI()
        self.assertFalse(api.auth)
        auth = RestAuthBasic('username', 'secretpw')
        api.auth = auth
        self.assertTrue(api.auth)

    def test_init_empty(self):
        api1 = RestyAPI(REST_URL, REST_AUTH_TOKEN)
        api2 = RestyAPI(REST_URL, REST_AUTH_TOKEN)
        api3 = RestyAPI(REST_URL, REST_AUTH_TOKEN)
        api = RestyAPI(REST_URL, REST_AUTH_TOKEN)
        self.assertEquals(api.resources, {})
        self.assertEquals(api.url, REST_URL)
        self.assertEquals(api.auth.token, REST_AUTH_TOKEN)

    def test_url_token(self):
        api = RestyAPI('//' + REST_URL + '///', REST_AUTH_TOKEN)
        self.assertEquals(api.url, REST_URL)
        self.assertEquals(api.auth.token, REST_AUTH_TOKEN)


if __name__ == '__main__':
    main()
