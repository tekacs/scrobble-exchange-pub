import warnings
from hashlib import md5 as _md5

import requests
import types

__all__ = ['Server']

class Server(object):
    _base_endpoint = 'http://ws.audioscrobbler.com/2.0/'
    _base_params = {'format': 'json'}

    def __init__(self, api_key, user=None, session_key=None):
        self._base_params.update(api_key=api_key)
#        [self._base_params.update({v: locals()[v]}) for v in ('user', 'session_key') if not v is None]
        if not user is None:
            self._base_params['user'] = user
        if not session_key is None:
            self._base_params['sk'] = session_key

    @property
    def api_key(self):
        return self._base_params['api_key']

    @property
    def user(self):
        return self._base_params['user']

    @property
    def session_key(self):
        return self._base_params['sk']

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

class APIMeta(type):
    """Define all possible methods on the class at creation-time."""
    def __new__(mcls, name, bases, attrs):
        cls = type.__new__(mcls, name, bases, attrs)
        local_getattr = types.UnboundMethodType(cls, mcls._get_attr)
        for method in attrs['_methods']:
            attrs[mcls._camelcase_to_underscores(method)] = local_getattr
        attrs['_name'] = name
        return cls

    @staticmethod
    def _camelcase_to_underscores(name):
        return ''.join(['_' + char.lower() if char.isupper() else char for char in name])

    @staticmethod
    def _get_attr(self, method, type='read', **kwargs):
        def _default_transformer(self, json_dict):
            json_dict['body_text'] = json_dict.pop('#text')
            return type('anon', (APIResponse,), json_dict)
        json_dict = getattr(self._server, type)(namespace=self._name, **kwargs)
        trans = _default_transformer
        if method in self._transformers: # robots in disguise!
            trans = self._transformers[method]
        return trans(json_dict)

class APIObject(object):
    pass

def transformer(cls, type='read'):
    def dec(f):
        if not f.func_name in cls._methods:
            warnings.warn('Tried to define transformer ' + f.func_name + ' - not in _methods!')
        cls._transformers[f.func_name] = f

        return f
    return dec

class APIResponse(object):
    pass
