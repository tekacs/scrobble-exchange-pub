# -*- coding: utf-8 -*-

__author__ = 'Amar Sood (tekacs)'

from .lastfm import LastFMAPIObject, APIMeta

class User(LastFMAPIObject):
    """A map to the last.fm User namespace."""

    __metaclass__ = APIMeta
    # _methods generated by lastfm._auth_filter
    _methods = {
        'get': [
            'getArtistTracks',
            'getBannedTracks',
            'getEvents',
            'getFriends',
            'getInfo',
            'getLovedTracks',
            'getNeighbours',
            'getNewReleases',
            'getPastEvents',
            'getPersonalTags',
            'getPlaylists',
            'getRecentTracks',
            'getShouts',
            'getTopAlbums',
            'getTopArtists',
            'getTopTags',
            'getTopTracks',
            'getWeeklyAlbumChart',
            'getWeeklyArtistChart',
            'getWeeklyChartList',
            'getWeeklyTrackChart',
            'signUp',
            'terms'
        ],
        'post': [
            'getRecentStations',
            'getRecommendedArtists',
            'getRecommendedEvents',
            'shout'
        ]
    }