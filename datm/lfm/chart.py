# -*- coding: utf-8 -*-

__author__ = 'Amar Sood (tekacs)'

from .lastfm import LastFMAPIObject, APIMeta

class Chart(LastFMAPIObject):
    """A map to the last.fm Chart namespace."""

    __metaclass__ = APIMeta
    _methods = {
        'get': [
            'getHypedArtists',
            'getHypedTracks',
            'getLovedTracks',
            'getTopArtists',
            'getTopTags',
            'getTopTracks'
        ],
        'post': []
    }