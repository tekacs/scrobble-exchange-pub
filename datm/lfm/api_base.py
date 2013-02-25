# -*- coding: utf-8 -*-
"""A somewhat generic set of (meta)classes to set up a map to a REST API.

@todo: Add a way to create input/request transformers as well as response ones.
(notably to allow users to pass params as True/False in place of 1/0, etc.)

@todo: There remain some last.fm-specific conventions in here, which could be
factored out with relatively little difficulty.
"""

__author__ = 'Amar Sood (tekacs)'

import pprint
from hashlib import md5 as _md5
from functools import wraps as _wraps

import requests

__all__ = ['APIMeta']

class APIClient(object):
    """Provides ``classmethod`` network services to ``APIObject``s.

    @todo: This is substantially more tied-in to last.fm-specifics (signatures!)
            than I would like. :/ Fix this.
    """
    _base_endpoint = 'http://ws.audioscrobbler.com/2.0/'
    _base_params = {'format': 'json'}

    @classmethod
    def _sign(cls, params):
        secret = params.pop('api_secret')
        sig = ''
        for k in sorted(params.iterkeys()):
            if k not in ('format', 'callback'):
                sig += k + str(params[k])
        sig += secret
        params['api_sig'] = _md5(sig).hexdigest()

    @classmethod
    def request(cls, method, http_method, sign=False, **params):
        request_kind = getattr(requests, http_method)
        params.update(cls._base_params)
        params.update(method=method)
        if params.pop('_debug', False):
            pprint.pprint(locals())
        if sign:
            cls._sign(params)
        r = request_kind(cls._base_endpoint, params=params).json()
        return r

class APIError(Exception):
    pass

class APIMeta(type):
    """A metaclass base for API objects. Provides:

    - Methods for all API methods listed in ``_methods['get']`` and
        ``_methods['post']`` on the class being instantiated, with the case of
        the generated methods converted to ``underscore_case`` from
        ``camelCase``.
    - The default transformer for JSON data returned for the API that passes
        validation and isn't an error, but for which a transformer has not been
        written.
    - An error handler to convert API errors to Python Exceptions.
    """

    def __new__(mcls, name, bases, attrs):
        """See class docstring."""
        try:
            for http_method in ('get', 'post'):
                for method in attrs['_methods'][http_method]:
                    ac = classmethod(mcls._api_call_maker(
                        method,
                        http_method,
                        attrs)
                    )
                    attrs[mcls._camelcase_to_underscores(method)] = ac
        except KeyError:
            raise SyntaxError('''Incorrectly derived API class!
            You must define _methods[\'get\'] and _methods[\'post\'].''')
        return type.__new__(mcls, name, bases, attrs)

    @classmethod
    def _api_call_maker(mcls, method, http_method, attrs):
        """This is a kludge to get around Python closure/scoping rules. :/"""
        transformer = attrs.get(
            mcls._camelcase_to_underscores(method),
            mcls.default_transformer
        )
        def api_call(cls, dictargs=(), **kwargs):
            kwargs.update(dictargs)
            json = APIClient.request(
                cls.__name__.lower() + '.' + method,
                http_method,
                http_method == 'post',
                **kwargs
            )
            if 'error' in json:
                return mcls.error_handler(cls, json)
            else:
                return transformer(json)
        return api_call

    @staticmethod
    def _camelcase_to_underscores(name):
        """Convert a camelCase string to underscore_case.

        4.4us timeit on 'getTrackInfo'
        """
        return ''.join('_' + char.lower() if char.isupper() else char
            for char in name)

    @staticmethod
    def _underscores_to_camelcase(name):
        """Convert an underscore_case string to camelCase.

        8.7us timeit on 'get_track_info'
        """
        name = list(name)
        return ''.join(name.pop(i+1).upper() if name[i] == '_' else name[i]
            for i in range(len(name)) if i < len(name))

    @staticmethod
    def default_transformer(json):
        """The default transformer for data received from the API.

        By default this uses the dotmagic class defined later in this file.
        """
        return json

    @staticmethod
    def error_handler(cls, json):
        """Convert API errors (from JSON) into Python Exceptions."""
        errors = cls._errors
        kind = int(json.pop('error'))
        message = "\n".join((json.pop('message'), pprint.pformat(json)))
        raise errors[kind](message)

# And now begins the magic...
# Beware of Python(ism)s

class frozendict(dict):
    '''A frozen dictionary class that can be hashed and indeed has hashing
        behaviour similar to the native behaviour (in PyPy, at least :P).

        Please note that this dict isn't _actually_ frozen. Doing so would
        require effort upon instantiation (you can't use metaclasses to
        customise builtin class creation (given that they're actually written
        and instantiated in C) afaik) and since the very point of this class
        is performance, I don't bother with that.

        The name is more of a hint to warn the user not to mess with it after
        creation, as doing so would invalidate the hash, which will not be
        updated appropriately.

        It would be quite trivially possible to extend this to include hash
        recalculation but again: *performance*.'''
    __slots__ = ('_hash',)
    def __hash__(self):
        ret = getattr(self, '_hash', None)
        if ret is None:
            ret = self._hash = hash(frozenset(self.iteritems()))
        return ret

def memoise(f):
    f.memo = memo = {}
    @_wraps(f)
    def wrapper(*args, **kwargs):
        uniq = (args, frozendict(kwargs))
        ret = memo.get(uniq)
        if ret is None:
            ret = memo[uniq] = f(*args, **kwargs)
        return ret
    return wrapper

def recursive_wrap(attr):
    def decorator(f):
        @_wraps(f)
        def wrapper(self, *args, **kwargs):
            if getattr(self, attr, False):
                return type(self)(f(self, *args, **kwargs), recursive=True)
            else:
                return f(self, *args, **kwargs)
        return wrapper
    return decorator

class dotmagic(object):
    """Django templates do this for dot lookup.

    I thought it was cool, so I implemented something like it.

    Essentially makes attributes, 'no-argument' method calls and dictionary
    accesses all possible homogeneously via attribute access or dictionary
    access.

    The order of lookup is dict > callable, 'no-arg' attr > straight attr.
    """

    def __init__(self, target, recursive=False):
        self.__target = target
        self.__recursive = recursive

    @recursive_wrap('_dotmagic__recursive')
    def __getval(self, name):
        target = self.__target

        try:
            return target[name]
        except (KeyError, TypeError, IndexError):
            pass

        try:
            return getattr(target, name)()
        except (AttributeError, TypeError):
            pass

        try:
            return getattr(target, name)
        except AttributeError:
            pass

        raise AttributeError(name)

    __getattr__ = __getval
    __getitem__ = __getval

    def __dir__(self):
        target = self.__target

        if callable(getattr(target, 'keys', None)):
            return target.keys()

        return dir(target)

    def __call__(self):
        """Gets the target value without recursively wrapping."""
        return self.__target