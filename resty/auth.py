#!/usr/bin/env python
"""
Module Resty

Date: November 25, 2013
Company: SwissTech Consulting.
Author: Patrick Glass <patrickglass@gmail.com>
Copyright: Copyright 2013 SwissTech Consulting.

Metric Server Error and Exceptions
"""
import base64

class RestAuth(object):

    def __init__(self):
        self.is_authenticated = False
        self.header = {}

    def getHeaders(self):
        return self.header


class RestAuthBasic(RestAuth):

    def __init__(self, username=None, password=None):
        super(RestAuthBasic, self).__init__()
        if not username or not password:
            raise ValueError("username and password must be supplied!")
        self.userpass = base64.b64encode('%s:%s' % (username, password))
        self.header = {
            'Authorization': 'Basic ' + self.userpass,
        }


class RestAuthToken(RestAuth):

    def __init__(self, token=None):
        super(RestAuthToken, self).__init__()
        if not token:
            raise ValueError("token must be set to a valid HTTP_Authorization token!")
        self.token = token
        self.header = {
            'Authorization': 'Token ' + self.token,
        }
