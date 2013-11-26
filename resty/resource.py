#!/usr/bin/env python
"""
Module Resty

Date: November 25, 2013
Company: SwissTech Consulting.
Author: Patrick Glass <patrickglass@gmail.com>
Copyright: Copyright 2013 SwissTech Consulting.

Resource Definition
"""

class ParentResource(object):
    pass

BASEPARENT = ParentResource()

class RestResource(object):

    def __init__(self, url, parent=BASEPARENT):
        self.meta_url = url
        self.meta_name = None
        self.meta_description = None
        self.meta_renders = []
        self.meta_parses = []
        self.meta_actions = {
            'GET': {},
            'POST': {},
            'PUT': {},
            'PATCH': {},
            'DELETE': {},
        }
        self.meta_parent = parent

    def one(self, pk):
        return RestResource(self.meta_url + str(pk) + '/')

    def all(self):
        return self
