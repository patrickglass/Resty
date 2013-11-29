"""
Resource Manager
"""
import httplib
import urllib
from resty.request import request

USER_AGENT = "Python-Resty/1.0"

class RestResource(object):

    def __init__(self, url, parent=None):
        self._url = url
        self._name = None
        self._description = None
        self._renders = []
        self._parses = []
        self._actions = {
            'GET': {},
            'POST': {
                "groups": {
                    "type": "field",
                    "required": False,
                    "read_only": True
                },
                "username": {
                    "type": "string",
                    "required": True,
                    "read_only": True,
                    "label": "username",
                    "help_text": "Required. 30 characters or fewer. Letters, numbers and @/./+/-/_ characters",
                    "max_length": 30
                },
            },
            'PUT': {},
            'PATCH': {},
            'DELETE': {},
        }
        self._parent = parent

        # HTTP Request settings
        # self.headers = {'User-Agent': USER_AGENT}
        # self.scheme, self.host, self.url, z1, z2 = httplib.urlsplit(self.api.base_url + self.uri)

        # Result information
        self._entries = {}
        self._count = 0
        self._index = 0
        # Fetch the validation settings here
        self._get_options()

    def _get_options(self):
        # data = request(self.url, 'OPTIONS', headers).read()
        # options = json.loads(data)
        options = {
            "name": "User List",
            "description": "A viewset for viewing and editing user instances.",
            "renders": [
                "application/json",
                "text/html"
            ],
            "parses": [
                "application/json",
                "application/x-www-form-urlencoded",
                "multipart/form-data"
            ],
            "actions": {
                "POST": {
                    "id": {
                        "type": "integer",
                        "required": False,
                        "read_only": True,
                        "label": "ID"
                    },
                    "url": {
                        "type": "field",
                        "required": False,
                        "read_only": True
                    },
                    "profile": {
                        "type": "field",
                        "required": True,
                        "read_only": True
                    },
                    "groups": {
                        "type": "field",
                        "required": False,
                        "read_only": True
                    },
                    "username": {
                        "type": "string",
                        "required": True,
                        "read_only": True,
                        "label": "username",
                        "help_text": "Required. 30 characters or fewer. Letters, numbers and @/./+/-/_ characters",
                        "max_length": 30
                    },
                    "first_name": {
                        "type": "string",
                        "required": False,
                        "read_only": True,
                        "label": "first name",
                        "max_length": 30
                    },
                    "last_name": {
                        "type": "string",
                        "required": False,
                        "read_only": True,
                        "label": "last name",
                        "max_length": 30
                    },
                    "email": {
                        "type": "email",
                        "required": False,
                        "read_only": True,
                        "label": "email address",
                        "max_length": 75
                    },
                    "is_staff": {
                        "type": "boolean",
                        "required": False,
                        "read_only": True,
                        "label": "staff status",
                        "help_text": "Designates whether the user can log into this admin site."
                    },
                    "is_active": {
                        "type": "boolean",
                        "required": False,
                        "read_only": True,
                        "label": "active",
                        "help_text": "Designates whether this user should be treated as active. Unselect this instead of deleting accounts."
                    },
                    "is_superuser": {
                        "type": "boolean",
                        "required": False,
                        "read_only": True,
                        "label": "superuser status",
                        "help_text": "Designates that this user has all permissions without explicitly assigning them."
                    },
                    "last_login": {
                        "type": "datetime",
                        "required": True,
                        "read_only": True,
                        "label": "last login"
                    },
                    "date_joined": {
                        "type": "datetime",
                        "required": True,
                        "read_only": True,
                        "label": "date joined"
                    }
                }
            }
        }
        # for res in resources:
        #     self.resource(res)

    def one(self, pk):
        return self[pk]

    def all(self):
        return self

    def __iter__(self):
        return self

    def next(self):
        if self._index >= self._count:
            raise StopIteration
        else:
            entry = self._entries[self._index]
            self._index += 1
            return entry

    def __getitem__(self, pk):
        try:
            entry = self._entries[pk]
        except KeyError, e:
            # Fetch the value from the server
            entry = RestResource(self._url_one(pk), self)
            self._entries[pk] = entry
            return entry

    def _url_one(self, pk):
        return self._url + str(pk) + '/'

    def _request(self, method, url, body={}, headers={}, meta={}):
        return request.request(method, url, data=data, headers=headers)
