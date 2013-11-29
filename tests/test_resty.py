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


def mock_response(content, headers='', url=REST_URL, code=200, msg='OK'):
    """
    Patch the urllib2.urlopen so we always control the output
    This method will now return what is specified in the obj.meta.response
    """
    # print "INFO: urllib2.urlopen is being mocked!"
    resp = urllib2.addinfourl(StringIO(str(content)), headers, url, code)
    resp.msg = msg
    return resp

class TestRestyUrlMock(TestCase):

    @patch('urllib2.urlopen')
    def test_request_root(self, mock_urlopen):
        """Test the mocking function to ensure we can fake urlib requests"""
        mock_data = 'here is some data'
        mock_urlopen.return_value = mock_response(mock_data)
        response = urllib2.urlopen(REST_URL)
        self.assertEqual(response.read(), mock_data)
        self.assertEqual(response.code, 200)
        self.assertEqual(response.msg, 'OK')


class TestRestyRootResource(TestCase):

    def setUp(self):
        # self.patcher = patch('resty.request.urllib2.urlopen')
        self.patcher = patch('urllib2.urlopen')
        self.mock_urlopen = self.patcher.start()
        self.content = """
        {
            "userprofiles": "http://localhost/api/userprofiles/",
            "users": "http://localhost/api/users/",
            "api-token": "http://localhost/api/token/",
            "comps": "http://localhost/api/components/",
            "reporttype": "http://localhost/api/reporttypes/",
            "groups": "http://localhost/api/groups/",
            "permissions": "http://localhost/api/permissions/",
            "reportsource": "http://localhost/api/reportsources/",
            "contenttype": "http://localhost/api/contenttype/",
            "reports": "http://localhost/api/reports/",
            "workspace": "http://localhost/api/workspaces/",
            "release": "http://localhost/api/releases/"
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

    # def test_api_request(self):
    #     self.assertEqual(request(REST_URL).code, 200)
    #     self.assertEqual(request(REST_URL).msg, 'OK')
    #     data = json.loads(request(REST_URL).read())
    #     self.assertEqual(data, json.loads(self.content))

    def test_api_discover(self):
        self.api.discover()
        for item in self.api.list_resources():
            # self.assertIn(item, expected_resources)
            self.assertTrue(item in self.expected_resources)


class TestRestyResourceInstance(TestCase):

    def setUp(self):
        # self.patcher = patch('resty.request.urllib2.urlopen')
        self.patcher = patch('urllib2.urlopen')
        self.mock_urlopen = self.patcher.start()
        self.content = """
        {
            "id": 1,
            "url": "http://localhost/api/users/1/",
            "profile": "http://localhost/api/userprofiles/1/",
            "groups": [],
            "username": "tomsawyer",
            "first_name": "Tom",
            "last_name": "Sawyer",
            "email": "Tom.Sawyer@example.com",
            "is_staff": true,
            "is_active": true,
            "is_superuser": false,
            "last_login": "2013-11-26T07:15:27Z",
            "date_joined": "2012-05-08T21:23:50Z"
        }
        """
        self.mock_urlopen.return_value = mock_response(self.content)
        self.api = RestyAPI(REST_URL, REST_AUTH_TOKEN)
        self.expected_resources = [
            u"userprofiles",
            u"users",
            u"api-token",
            u"components",
            u"reporttype",
            u"groups",
            u"permissions",
            u"reportsource",
            u"contenttype",
            u"reports",
            u"workspace",
            u"release"
        ]

    # @skip("not implemented yet")
    def test_get_one(self):
        c = self.api.resource('users')
        user = c.one(1)
        # self.assertEqual(user.id, 1)
        # self.assertEqual(user.url, 'http://localhost/api/users/1/')
        # self.assertEqual(user.profile, 'http://localhost/api/userprofiles/1/')
        # self.assertEqual(user.groups, [])
        # self.assertEqual(user.username, 'tomsawyer')
        # self.assertEqual(user.first_name, 'Tom')
        # self.assertEqual(user.last_name, 'Sawyer')
        # self.assertEqual(user.email, 'Tom.Sawyer@example.com')
        # self.assertTrue(user.is_staff)
        # self.assertTrue(user.is_active)
        # self.assertFalse(user.is_superuser)
        # self.assertEqual(user.last_login, '2013-11-26T07:15:27Z')
        # self.assertEqual(user.date_joined, '2012-05-08T21:23:50Z')

if __name__ == '__main__':
    print "INFO: Running tests for resty api class!"
    main()

