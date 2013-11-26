#!/usr/bin/env python
"""
Module Resty

Date: November 25, 2013
Company: SwissTech Consulting.
Author: Patrick Glass <patrickglass@gmail.com>
Copyright: Copyright 2013 SwissTech Consulting.

UnitTest framework for validating the Resty system
"""
import os
import sys
import unittest2
sys.path.append(os.path.join(os.path.dirname(__file__), "../resty/"))

from test_resty import *

if __name__ == '__main__':
    print "INFO: Running tests for Resty library!"
    unittest.main()
