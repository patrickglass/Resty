"""
Module Resty

Date: November 25, 2013
Company: SwissTech Consulting.
Author: Patrick Glass <patrickglass@gmail.com>
Copyright: Copyright 2013 SwissTech Consulting.

This class implements a simple rest api framework for interfacing with the
Server via its REST API.
"""
__title__ = 'Resty'
__version__ = '0.1'
__author__ = 'Patrick Glass'
__license__ = 'Apache 2.0'
__copyright__ = 'Copyright 2013 Patrick Glass'

from resty.api import RestyAPI
from resty.exceptions import (
    RestApiException,
    RestApiUrlException,
    RestApiAuthError,
    RestApiBadRequest,
    RestApiServersDown
)
from resty.auth import RestAuthToken
from resty.request import request
