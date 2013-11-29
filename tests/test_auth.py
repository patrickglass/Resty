#!/usr/bin/env python
"""
UnitTest framework for validating the Resty system
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "../"))
from unittest import TestCase, main

from resty.auth import RestAuth, RestAuthBasic, RestAuthToken

class TestRestyAuth(TestCase):
    def test_auth_init(self):
        auth = RestAuth()
        self.assertEqual(auth.headers, {})
        self.assertEqual(auth.is_authenticated, False)

    def test_auth_ok(self):
        auth = RestAuthBasic('Aladdin', 'open sesame')
        self.assertEqual(auth.headers, {
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
        self.assertEqual(auth.headers, {
            'Authorization': 'Token MYSECRETTOKEN',
        })
        self.assertEqual(auth.is_authenticated, False)

    def test_tokenauth_missing_token(self):
        self.assertRaises(ValueError, RestAuthToken)
        self.assertRaises(ValueError, RestAuthToken, '')


if __name__ == '__main__':
    main()
