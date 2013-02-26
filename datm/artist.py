__author__ = 'amar'

import lfm
import models

from util import db, lastfm
from util.magic import memoised_property
from base import DATMObject, datm_setup, NoDatabaseObjectException
from config import require_data_source, require_lastfm, require_db

class Artist(DATMObject):
    @datm_setup
    def __init__(self, name=None, mbid=None):
        if (mbid is None) and (name is None):
            raise TypeError('Artist requires a \'name\' or an \'MBID\'')
        if mbid is not None:
            correction = lfm.Artist.get_correction(lastfm.params(artist=name))
            if not correction.get('status', None) == 'ok':
                name = correction['name']
                mbid = correction['mbid']
        else:
            self._mbid = mbid


    @memoised_property
    @require_db
    def dbo(self):
        return db.query(
            self.config,
            models.Artist
        ).filter(models.Artist.mbid == self.mbid).one()

    @staticmethod
    @require_lastfm
    def api_search(config, name, limit=5, page=1):
        lfm.Artist.search(lastfm.params(artist=name, limit=limit, page=page))

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

    @memoised_property
    @require_data_source
    def name(self):
        return self._name

    @memoised_property
    @require_data_source
    def mbid(self):
        return self._mbid

    @memoised_property
    @require_lastfm
    def images(self):
        pass

    @property
    @require_db
    def price(self):
        pass

    @property
    @require_db
    def points(self):
        pass

    @property
    @require_db
    def no_remaining(self):
        pass

    @property
    @require_db
    def max_available(self):
        pass

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