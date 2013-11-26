#!/usr/bin/env python
"""
Module Resty

Date: November 25, 2013
Company: SwissTech Consulting.
Author: Patrick Glass <patrickglass@gmail.com>
Copyright: Copyright 2013 SwissTech Consulting.

This class implements a simple rest api framework for interfacing with the
Server via its REST API.
"""
from .api import RestyAPI
from .exceptions import (
    RestApiException,
    RestApiUrlException,
    RestApiAuthError,
    RestApiBadRequest,
    RestApiServersDown
)
from .auth import RestAuthToken
from .request import request
