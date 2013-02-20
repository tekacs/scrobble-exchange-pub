__author__ = 'amar'

import models

from base import DATMObject
from config import require_data_source, require_lastfm, require_db

class Artist(DATMObject):
    def __init__(self, name=None, mbid=None):
        if (mbid is None) and (name is None):
            raise TypeError('Artist requires a \'name\' or an \'MBID\'')
        if mbid is not None:
            self._mbid = mbid
        if name is not None:
            self._name = name

    @staticmethod
    @require_lastfm
    def api_search(limit=5):
        pass

    @staticmethod
    @require_lastfm
    def popular(limit=10):
        pass

    @staticmethod
    @require_db
    def top(limit=10):
        pass

    @staticmethod
    @require_db
    def most_traded(limit=10):
        pass

    @property
    @require_data_source
    def name(self):
        return self._name

    @property
    @require_data_source
    def mbid(self):
        return self._mbid

    @property
    @require_lastfm
    def images(self):
        pass

    @property
    @require_db
    def price(self):
        pass

    @property
    @require_db
    def no_remaining(self):
        pass

    @property
    @require_db
    def max_available(self):
        pass

    @property
    @require_db
    def history(self, after, step=None):
        pass

    @property
    @require_lastfm
    def streamable(self):
        pass

    @property
    @require_lastfm
    def listeners(self):
        pass

    @property
    @require_lastfm
    def plays(self):
        pass

    @property
    @require_lastfm
    def similar(self):
        pass

    @property
    @require_lastfm
    def bio(self):
        pass

class NoStockRemainingException(Exception):
    pass