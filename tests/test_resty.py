#!/usr/bin/env python
"""
Company: SwissTech Consulting.
Author: Patrick Glass <patrickglass@gmail.com>
Copyright: Copyright 2013 SwissTech Consulting.

UnitTest framework for validating the Resty system
"""
import sys
import os
import time
import unittest
from mock import patch
sys.path.append(os.path.join(os.path.dirname(__file__), "../pmcx/"))

import logging
import random
import urllib2
import json
from StringIO import StringIO
from resty.api import RestyAPI, RestApiException, RestApiAuthError
from resty.auth import RestAuth, RestAuthBasic, RestAuthToken


REST_HOST = 'localhost:8080'
REST_URL = 'http://' + REST_HOST + '/api/v1/'
REST_AUTH_TOKEN = 'AUTH_TOKEN_GOES_HERE'


def mock_response(content, headers='', url=REST_URL, code=200, msg='OK'):
    """
    Patch the urllib2.urlopen so we always control the output
    This method will now return what is specified in the obj.meta.response
    """
    resp = urllib2.addinfourl(StringIO(str(content)), headers, url, code)
    # resp.code = 200
    resp.msg = msg
    # print "INFO: urllib2.urlopen is being mocked!"
    return resp


class TestRestyAuth(unittest.TestCase):
    def test_auth_init(self):
        auth = RestAuth()
        self.assertEqual(auth.getHeaders(), {})
        self.assertEqual(auth.is_authenticated, False)

    def test_auth_ok(self):
        auth = RestAuthBasic('Aladdin', 'open sesame')
        self.assertEqual(auth.getHeaders(), {
            'Authorization': 'Basic QWxhZGRpbjpvcGVuIHNlc2FtZQ==',
        })
        self.assertEqual(auth.is_authenticated, False)

    def test_basicauth_badinput(self):
        self.assertRaises(ValueError, RestAuthBasic, 'Aladdin', '')

    def test_basicauth_badinput2(self):
        self.assertRaises(ValueError, RestAuthBasic, '', '')

    def test_basicauth_badinput2(self):
        self.assertRaises(ValueError, RestAuthBasic)

    def test_tokenauth_ok(self):
        auth = RestAuthToken('MYSECRETTOKEN')
        self.assertEqual(auth.getHeaders(), {
            'Authorization': 'Token MYSECRETTOKEN',
        })
        self.assertEqual(auth.is_authenticated, False)

    def test_tokenauth_missing_token(self):
        self.assertRaises(ValueError, RestAuthToken)
        self.assertRaises(ValueError, RestAuthToken, '')


class TestRestyInit(unittest.TestCase):

    def test_no_args(self):
        self.assertRaises(TypeError, RestyAPI)

    def test_url(self):
        self.assertRaises(ValueError, RestyAPI, REST_URL)

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

    @patch('urllib2.urlopen')
    def test_request_root(self, mock_urlopen):
        """Test the mocking function to ensure we can fake urlib requests"""
        mock_data = 'here is some data'
        mock_urlopen.return_value = mock_response(mock_data)
        response = urllib2.urlopen(REST_URL)
        self.assertEqual(response.read(), mock_data)
        self.assertEqual(response.code, 200)
        self.assertEqual(response.msg, 'OK')


class TestRestyRootResource(unittest.TestCase):

    # @patch('resty.api.urllib2.urlopen')
    # def setUp(self, mock_urlopen):
    def setUp(self):
        self.patcher = patch('resty.api.urllib2.urlopen')
        self.mock_urlopen = self.patcher.start()
        self.content = """
        {
            "userprofiles": "http://metrics:8080/api/userprofiles/",
            "users": "http://metrics:8080/api/users/",
            "api-token": "http://metrics:8080/api/token/",
            "comps": "http://metrics:8080/api/components/",
            "reporttype": "http://metrics:8080/api/reporttypes/",
            "groups": "http://metrics:8080/api/groups/",
            "permissions": "http://metrics:8080/api/permissions/",
            "reportsource": "http://metrics:8080/api/reportsources/",
            "contenttype": "http://metrics:8080/api/contenttype/",
            "reports": "http://metrics:8080/api/reports/",
            "workspace": "http://metrics:8080/api/workspaces/",
            "release": "http://metrics:8080/api/releases/"
        }
        """
        self.mock_urlopen.return_value = mock_response(self.content)
        self.api = RestyAPI(REST_URL, REST_AUTH_TOKEN)
        self.expected_resources = [
            u"userprofiles",
            u"users",
            u"api-token",
            u"comps",
            u"reporttype",
            u"groups",
            u"permissions",
            u"reportsource",
            u"contenttype",
            u"reports",
            u"workspace",
            u"release"
        ]

    def test_api_request(self):
        self.assertEqual(self.api.request(REST_URL).code, 200)
        self.assertEqual(self.api.request(REST_URL).msg, 'OK')
        data = json.loads(self.api.request(REST_URL).read())
        self.assertEqual(data, json.loads(self.content))

    def test_api_discover(self):
        self.api.discover()
        for item in self.api.resources.keys():
            # self.assertIn(item, expected_resources)
            self.assertTrue(item in self.expected_resources)




if __name__ == '__main__':
    print "INFO: Running tests for resty api class!"
    unittest.main()

