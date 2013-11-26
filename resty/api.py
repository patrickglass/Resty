#!/usr/bin/python -tt
# -*- coding: utf-8 -*-
"""
Module Resty

Date: November 25, 2013
Company: SwissTech Consulting.
Author: Patrick Glass <patrickglass@gmail.com>
Copyright: Copyright 2013 SwissTech Consulting.

This class implements a simple rest api framework for interfacing with the
Server via its REST API.
"""
import socket
import httplib
import urllib2
import json

from .exceptions import (
    RestApiException,
    RestApiUrlException,
    RestApiAuthError,
    RestApiBadRequest,
    RestApiServersDown
)
from .resource import RestResource
from .auth import RestAuthToken


class RestyAPI(object):
    """
    Used to easily consume a django-rest-framework compatable API.
    it can discover all the resources automatically and imports the field
    validation.
    """

    def __init__(self, baseUrl, token=None):
        self.resources = {}
        self.setBaseUrl(baseUrl)
        self.setAuth(RestAuthToken, token=token)
        self.headers = {
            'Content-Type': 'application/json'
        }


    def setBaseUrl(self, baseUrl):
        if not baseUrl:
            raise ValueError("baseUrl must be a full URL to the base API!")
        self.url = baseUrl.strip('/') + '/'


    def setAuth(self, authMethod, **kwargs):
        if not authMethod:
            raise ValueError("baseUrl must be a full URL to the base API!")
        self.auth = authMethod(**kwargs)

    def resource(self, name):
        """
        Creates an object to consume a resource on a remote REST API
        eg. api.resource(name).one(id)
            will GET on /{name}/{id}/
        """
        if name in self.resources:
            res = self.resources[name]
        else:
            url = self.url + '/' + name.strip('/') + '/'
            res = RestResource(url)
            self.resources[name] = res
        return res

    def discover(self):
        """
        Will use the baseURL and query the remote server to auto determine
        the resources and the field validation for each resource
        """
        data = self.request(self.url).read()
        resources = json.loads(data)
        for res in resources:
            self.resource(res)


    def request(self, url):
        # Get the global headers and set any extra headers
        headers = self.headers.copy()
        headers.update(self.auth.getHeaders())

        # req = urllib2.Request(url, str(headers))
        # resp = urllib2.urlopen(req)
        # # print resp.read()
        # # return resp

        # Perform the url request
        try:
            req = urllib2.Request(url, str(headers))
            resp = urllib2.urlopen(req)
            # print resp.read()
            return resp
        except urllib2.HTTPError as e:
            if e.code == 403 or e.code == 401:
                raise RestApiAuthError(e)
            elif e.code == 400:
                logging.error("%s: %s" % (e, e.read()))
                raise RestApiBadRequest(e)
            else:
                raise RestApiUrlException(e)
        except (urllib2.URLError, httplib.HTTPException) as e:
            raise RestApiUrlException(e)
        except Exception as e:
            raise RestApiException(e)
