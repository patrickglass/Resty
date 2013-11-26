#!/usr/bin/env python
"""
Company: SwissTech Consulting.
Author: Patrick Glass <patrickglass@gmail.com>
Copyright: Copyright 2013 SwissTech Consulting.

UnitTest framework for validating the Resty system
"""
import sys
import os
from unittest2 import TestCase

from resty.auth import RestAuth, RestAuthBasic, RestAuthToken

class TestRestyAuth(TestCase):
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


if __name__ == '__main__':
    unittest.main()
