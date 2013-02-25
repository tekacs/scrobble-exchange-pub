# -*- coding: utf-8 -*-

__author__ = 'Amar Sood (tekacs)'

from .lastfm import LastFMAPIObject, APIMeta

class Auth(LastFMAPIObject):
    """A map to the last.fm Auth namespace."""

    __metaclass__ = APIMeta
    _methods = {
        'get': [],
        'post': [
            'getMobileSession',
            'getSession',
            'getToken'
        ]
    }