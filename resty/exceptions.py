"""
Error and Exceptions
"""

class RestApiException(Exception):
    """
    Indicates a general Resty Exception.
    """
    def __init__(self, value):
        self.parameter = value

    def __str__(self):
        return repr(self.parameter)


class RestApiUrlException(Exception):
    """
    Indicates there was an issue with the urllib http request.
    """
    def __init__(self, value):
        self.parameter = value

    def __str__(self):
        return repr(self.parameter)


class RestApiBadRequest(Exception):
    """
    Raised when there was an ERROR 400 BAD REQUEST
    This usually occurs when the api is passed data that is not formatted
    as a correct json resource.
    """
    def __init__(self, value):
        self.parameter = value

    def __str__(self):
        return repr(self.parameter)


class RestApiServersDown(Exception):
    """
    Raised when the server could not be reached and the
    timeout and number of retries limit was reached.
    """
    def __init__(self, value):
        self.parameter = value

    def __str__(self):
        return repr(self.parameter)


class RestApiAuthError(Exception):
    """
    Raised when the provided user credentials were invalid or
    lacking permissions to access the resource.
    """
    def __init__(self, value):
        self.parameter = value

    def __str__(self):
        return repr(self.parameter)
