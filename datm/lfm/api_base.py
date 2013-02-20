import warnings
from hashlib import md5 as _md5
from functools import wraps as _wraps

import requests
import types

__all__ = ['Server']

class APIClient(object):
    _base_endpoint = 'http://ws.audioscrobbler.com/2.0/'
    _base_params = {'format': 'json'}

    def __init__(self, api_key, api_secret=None):
        """The basis for a last.fm API server connection:
            api_key (required) :: needed to perform any operations on the API.
            api_secret :: required to perform any authenticated operations on the API
        """
        self._base_params.update(api_key=api_key)
        if not api_secret is None:
            self._base_params['api_secret'] = api_secret

    @property
    def api_key(self):
        return self._base_params['api_key']

    @property
    def api_secret(self):
        try:
            return self._base_params['api_secret']
        except KeyError:
            raise AttributeError('api_secret')

    @api_secret.setter
    def api_secret(self, value):
        self._base_params['api_secret'] = value

    def _sign(self, params):
        sig = ''
        for k in sorted(params.iterkeys()):
            if k not in ('format', 'callback'):
                sig += k + str(params[k])
        params['api_sig'] = _md5(sig).hexdigest()

    def read(self, namespace, method, **params):
        params.update(self._base_params)
        return requests.get(self._base_endpoint, params=params).json()

    def write(self, namespace, method, **params):
        params.update(self._base_params)
        self._sign(params)
        return requests.post(self._base_endpoint, params=params).json()

class AuthClient(object):
    def __init__(self, user, session_key=None):
        self.user = user
        self.session_key = session_key

class APIMeta(type):
    """Define all possible methods on the class at creation-time."""
    def __new__(mcls, name, bases, attrs):
        cls = type.__new__(mcls, name, bases, attrs)
        local_getattr = types.UnboundMethodType(cls, mcls._get_attr)
        for method in attrs['_methods']:
            setattr(cls, mcls._camelcase_to_underscores(method), local_getattr)
        return cls

    @staticmethod
    def _camelcase_to_underscores(name):
        return ''.join(['_' + char.lower() if char.isupper() else char for char in name])

    @staticmethod
    def _get_attr(self, method, type='read', **kwargs):
        def _default_transformer(self, json_dict):
            json_dict['body_text'] = json_dict.pop('#text')
            return type(method, (APIResponse,), json_dict)
        json_dict = getattr(self._server, type)(namespace=self._name, **kwargs)
        trans = _default_transformer
        if method in self._transformers: # robots in disguise!
            trans = self._transformers[method]
        return trans(json_dict)

class APIObject(object):
    pass

def transformer(cls, type='read'):
    def decorator(f):
        if not f.func_name in cls._methods:
            warnings.warn('Tried to define transformer ' + f.func_name + ' - not in _methods!')
        cls._transformers[f.func_name] = f

        return f
    return decorator

class APIResponse(object):
    pass

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

    def __call__(self):
        """Gets the target value without recursively wrapping."""
        return self.__target