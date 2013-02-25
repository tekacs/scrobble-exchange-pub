# -*- coding: utf-8 -*-

__author__ = 'Amar Sood (tekacs)'

import requests
from collections import defaultdict

from .api_base import APIError, APIMeta

__all__ = [
    'TransientError',
    'AuthenticationError',
    'DataError',
    'ProgrammingError',
    'ServiceError',
    'LastFMAPIObject',
    'RequestBuilder'
]

# Error base types

class TransientError(APIError):
    """Base for transient errors (may disappear on an immediate retry)."""

class AuthenticationError(APIError):
    """Base for authentication-related errors (re-authenticate or forbidden)."""

class DataError(APIError):
    """Base for errors arising from invalid data passed to the API."""

class ProgrammingError(APIError):
    """Base for errors in the code of the application or this library."""

class ServiceError(APIError):
    """Base for show-stopper last.fm API errors that do not warrant retries."""

# Last.fm Errors

class GenericOperationFailure(TransientError):
    pass

class TemporaryError(TransientError):
    pass

class AuthenticationFailure(AuthenticationError):
    pass

class InvalidSessionKeyError(AuthenticationError):
    pass

class UnauthorisedTokenError(AuthenticationError):
    pass

class ExpiredTokenError(AuthenticationError):
    pass

class InvalidResourceError(DataError):
    pass

class InvalidAPIKeyError(DataError):
    pass

class NotLoggedInError(DataError):
    """No user credentials were passed.

    This is not an authentication error so much as it is a flaw in the data
    passed to the relevant API call."""

class InvalidServiceError(ProgrammingError):
    pass

class InvalidMethodError(ProgrammingError):
    pass

class InvalidFormatError(ProgrammingError):
    pass

class InvalidParametersError(ProgrammingError):
    pass

class InvalidMethodSignatureError(ProgrammingError):
    pass

class SuspendedAPIKeyError(ProgrammingError):
    pass

class DeprecatedMethodError(ProgrammingError):
    pass

class InvalidErrorError(ServiceError):
    """'This error does not exist'"""

class ServiceOffline(ServiceError):
    pass

class RateLimitError(ServiceError):
    pass

class LastFMAPIObject(object):
    """The base class for last.fm API namespace objects.

    Objects derived from this should use the metaclass ``APIMeta``.

    Does *not* include the errors associated with last.fm Radio.
    @todo: Add radio errors (12, 18, 20, 21, 22, 23, 24, 25)
    """

    _errors = defaultdict(InvalidErrorError)
    _errors.update({
        1: InvalidErrorError,
        2: InvalidServiceError,
        3: InvalidMethodError,
        4: AuthenticationFailure,
        5: InvalidFormatError,
        6: InvalidParametersError,
        7: InvalidResourceError,
        8: GenericOperationFailure,
        9: InvalidSessionKeyError,
        10: InvalidAPIKeyError,
        11: ServiceOffline,
        13: InvalidMethodSignatureError,
        14: UnauthorisedTokenError,
        15: ExpiredTokenError,
        16: TemporaryError,
        17: NotLoggedInError,
        19: InvalidErrorError,
        26: SuspendedAPIKeyError,
        27: DeprecatedMethodError,
        29: RateLimitError
    })

class RequestBuilder(object):
    """Aids in the construction of parameter dictionaries for API requests."""
    def __init__(self, api_key, api_secret=None, user=None, session_key=None):
        self._base_params = {
            'raw': 'true',
            'api_key': api_key
        }

        self._auth_params = {}
        params_map = {
            'api_secret': 'api_secret',
            'username': 'user',
            'sk': 'session_key'
        }
        for k, v in params_map.iteritems():
            if locals()[v] is not None:
                self._auth_params[k] = locals()[v]

    @property
    def api_key(self):
        return self._base_params['api_key']

    @api_key.setter
    def api_key(self, v):
        self._base_params['api_key'] = v

    @property
    def api_secret(self):
        return self._auth_params['api_secret']

    @api_secret.setter
    def api_secret(self, v):
        self._auth_params['api_secret'] = v

    @property
    def session_key(self):
        return self._auth_params['sk']

    @session_key.setter
    def session_key(self, v):
        self._auth_params['sk'] = v

    @property
    def user(self):
        return self._auth_params['user']

    @user.setter
    def user(self, v):
        self._auth_params['user'] = v

    def params(self, dictargs=(), **kwargs):
        kwargs.update(dictargs)
        kwargs.update(self._base_params)
        return kwargs

    def auth(self, dictargs=(), **kwargs):
        kwargs.update(dictargs)
        kwargs.update(self._auth_params)
        return kwargs

def _authfilter(str):
    """A handy helper to construct read/write lists for last.fm API methods."""
    get = []
    post = []
    base = 'http://www.last.fm/api/show/'
    [(post if 'authentication required' in requests.get(base + name).text else get).append(
        name[name.index('.')+1:]
    ) for name in str.split("\n")]
    return {'get': get, 'post': post}