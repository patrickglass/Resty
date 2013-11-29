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
REST_URL = 'http://' + REST_HOST + '/api/v1'
AUTH_TOKEN = 'f755f0351560620d837d8976e1f8a83480fbc2a0'

def request_wrapper(method, url, **kwargs):
    kwargs['allow_redirects'] = True
    resp = request(method, url, **kwargs)
    # print "RESP: (%s, %s)" %  (resp.status, resp.reason)
    # print resp
    # print resp.__dict__
    # print resp.getheaders()
    print resp.getheader('location')
    return resp


class TestRestyRequestRootRedirect(TestCase):

    def setUp(self):
        self.url = REST_URL

    def test_request_get(self):
        resp = request_wrapper('get', self.url)
        self.assertEqual(resp.status, 200)

    def test_request_options(self):
        resp = request_wrapper('options', self.url)
        self.assertEqual(resp.status, 200)

    def test_request_head(self):
        resp = request_wrapper('head', self.url)
        self.assertEqual(resp.status, 301)


class TestRestyRequestRootOK(TestCase):

    def setUp(self):
        self.url = REST_URL = '/'

    def test_request_get(self):
        resp = request_wrapper('get', self.url)
        self.assertEqual(resp.status, 200)

    def test_request_options(self):
        resp = request_wrapper('options', self.url)
        self.assertEqual(resp.status, 200)

    def test_request_head(self):
        resp = request_wrapper('head', self.url)
        self.assertEqual(resp.status, 301)


class TestRestyRequestRedirect5(TestCase):
    """Only Get and Options should allow redirection"""

    def setUp(self):
        self.url = 'http://httpbin.org/redirect/5'

    def test_request_get(self):
        resp = request_wrapper('get', self.url)

        self.assertEqual(resp.status, 200)

    def test_request_options(self):
        resp = request_wrapper('options', self.url)
        self.assertEqual(resp.status, 200)

    def test_request_head(self):
        resp = request_wrapper('head', self.url)
        self.assertEqual(resp.status, 301)

    def test_request_post(self):
        resp = request_wrapper('post', self.url)
        self.assertEqual(resp.status, 500)

    def test_request_put(self):
        resp = request_wrapper('put', self.url)
        self.assertEqual(resp.status, 301)

    def test_request_patch(self):
        resp = request_wrapper('patch', self.url)
        self.assertEqual(resp.status, 301)

    def test_request_delete(self):
        resp = request_wrapper('delete', self.url)
        self.assertEqual(resp.status, 301)

class TestRestyRequestRedirect50(TestCase):
    """Only Get and Options should allow redirection"""

    def setUp(self):
        self.url = 'http://httpbin.org/redirect/50'

    def test_request_get(self):
        resp = request_wrapper('get', self.url)

        self.assertEqual(resp.status, 301)

    def test_request_options(self):
        resp = request_wrapper('options', self.url)
        self.assertEqual(resp.status, 301)

    def test_request_head(self):
        resp = request_wrapper('head', self.url)
        self.assertEqual(resp.status, 301)

    def test_request_post(self):
        resp = request_wrapper('post', self.url)
        self.assertEqual(resp.status, 500)

    def test_request_put(self):
        resp = request_wrapper('put', self.url)
        self.assertEqual(resp.status, 301)

    def test_request_patch(self):
        resp = request_wrapper('patch', self.url)
        self.assertEqual(resp.status, 301)

    def test_request_delete(self):
        resp = request_wrapper('delete', self.url)
        self.assertEqual(resp.status, 301)


class TestRestyRequestRedirectLocalHost(TestCase):
    """Only Get and Options should allow redirection
    The num of restrictions is larger than allowed.
    All requests will return status 301"""

    def setUp(self):
        self.url = REST_URL + '/reports/500'
        print self.url

    def test_request_get(self):
        resp = request_wrapper('get', self.url)
        self.assertEqual(resp.status, 200)

    def test_request_options(self):
        resp = request_wrapper('options', self.url)
        self.assertEqual(resp.status, 200)

    def test_request_head(self):
        resp = request_wrapper('head', self.url)
        self.assertEqual(resp.status, 301)

    def test_request_post(self):
        resp = request_wrapper('post', self.url)
        self.assertEqual(resp.status, 500)

    def test_request_put(self):
        resp = request_wrapper('put', self.url)
        self.assertEqual(resp.status, 301)

    def test_request_patch(self):
        resp = request_wrapper('patch', self.url)
        self.assertEqual(resp.status, 301)

    def test_request_delete(self):
        resp = request_wrapper('delete', self.url)
        self.assertEqual(resp.status, 301)


class TestRestyRequestResourceListRedirect(TestCase):

    def setUp(self):
        self.url = REST_URL + '/reports'

    def test_request_get(self):
        resp = request_wrapper('get', self.url)
        self.assertEqual(resp.status, 200)

    def test_request_options(self):
        resp = request_wrapper('options', self.url)
        print resp.reason
        self.assertEqual(resp.status, 200)

    def test_request_head(self):
        resp = request_wrapper('head', self.url)
        self.assertEqual(resp.status, 301)

    # def test_request_post(self):
    #     resp = request_wrapper('post', self.url)
    #     self.assertEqual(resp.status, 500)


class TestRestyRequestResourceListOK(TestCase):

    def setUp(self):
        self.url = REST_URL + '/reports/'

    def test_request_get(self):
        resp = request_wrapper('get', self.url)
        self.assertEqual(resp.status, 200)

    def test_request_options(self):
        resp = request_wrapper('options', self.url)
        print resp.reason
        self.assertEqual(resp.status, 200)

    def test_request_head(self):
        resp = request_wrapper('head', self.url)
        self.assertEqual(resp.status, 301)

    # def test_request_post(self):
    #     resp = request_wrapper('post', self.url)
    #     self.assertEqual(resp.status, 500)


class TestRestyRequestResourceInstanceUnauthenticated(TestCase):

    def setUp(self):
        self.url = REST_URL + '/reports/500/'
        print self.url

    def test_request_get(self):
        resp = request_wrapper('get', self.url)
        self.assertEqual(resp.status, 200)

    def test_request_options(self):
        resp = request_wrapper('options', self.url)
        self.assertEqual(resp.status, 200)

    def test_request_head(self):
        resp = request_wrapper('head', self.url)
        self.assertEqual(resp.status, 200)

    def test_request_post(self):
        resp = request_wrapper('post', self.url)
        self.assertEqual(resp.status, 401)

    def test_request_put(self):
        resp = request_wrapper('put', self.url)
        self.assertEqual(resp.status, 401)

    def test_request_patch(self):
        resp = request_wrapper('patch', self.url)
        self.assertEqual(resp.status, 401)

    def test_request_delete(self):
        resp = request_wrapper('delete', self.url)
        self.assertEqual(resp.status, 401)

class TestRestyRequestResourceInstanceAuthenticated(TestCase):

    def setUp(self):
        self.url = REST_URL + '/reports/500/'
        self.auth_header = {
            'Authorization': 'Token ' + AUTH_TOKEN,
        }
        print self.url

    def test_request_get(self):
        resp = request_wrapper('get', self.url, headers=self.auth_header)
        self.assertEqual(resp.status, 200)

    def test_request_options(self):
        resp = request_wrapper('options', self.url, headers=self.auth_header)
        self.assertEqual(resp.status, 200)

    def test_request_head(self):
        resp = request_wrapper('head', self.url, headers=self.auth_header)
        self.assertEqual(resp.status, 200)

    def test_request_post(self):
        resp = request_wrapper('post', self.url, headers=self.auth_header)
        self.assertEqual(resp.status, 401)

    def test_request_put(self):
        resp = request_wrapper('put', self.url, headers=self.auth_header)
        self.assertEqual(resp.status, 401)

    def test_request_patch(self):
        resp = request_wrapper('patch', self.url, headers=self.auth_header)
        self.assertEqual(resp.status, 401)

    def test_request_delete(self):
        resp = request_wrapper('delete', self.url, headers=self.auth_header)
        self.assertEqual(resp.status, 401)

if __name__ == '__main__':
    main()

