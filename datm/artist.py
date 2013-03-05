__author__ = 'amar'

from functools import partial

from sqlalchemy import func
from sqlalchemy.orm.exc import NoResultFound

import lfm
import models

from util import db, lastfm
from util.magic import memoised_property, PartialDict
from base import DATMObject, datm_setup, NoDatabaseObjectException
from config import require_data_source, require_lastfm, require_db, has_lastfm,\
    NoDatabaseException, NoLastFMException

class Artist(DATMObject):
    @datm_setup
    def __init__(self,
                 config,
                 name=None,
                 mbid=None,
                 dbo=None,
                 lastfm_info=None):
        if dbo is not None:
            self.dbo = dbo
            return
        if lastfm_info is not None:
            self.lastfm_info = lastfm_info
            return
        if mbid is not None:
            self.mbid = mbid
            return
        if name is not None:
            correction = self.correct(self.config, name)
            if correction:
                self.name = correction['name']
                self.mbid = correction['mbid'] or self.mbid
            else:
                self.name = name

    # Primary Keys

    @memoised_property
    @require_data_source
    def name(self):
        try:
            return self.dbo.name
        except (NoDatabaseException, NoDatabaseObjectException):
            pass
        try:
            return self.lastfm_info['name']
        except (NoLastFMException, KeyError, AttributeError, TypeError):
            pass

        # In theory @require_data_source should prevent this from occurring.
        raise AttributeError('Artist object instantiated without name source.')

    @memoised_property
    def mbid(self):
        """Return the MBID corresponding to this object."""
        try:
            return self.lastfm_info['mbid']
        except (NoLastFMException, KeyError, AttributeError, TypeError):
            pass
        try:
            return self.dbo.mbid
        except (NoDatabaseException, NoDatabaseObjectException, AttributeError):
            pass

#       FIXME: Removed @require_data_source due to infinite recursion despite care :/
#        In theory @require_data_source should prevent this from occurring.
        raise AttributeError('Artist object instantiated without mbid source.')

    # Data Accessors

    @memoised_property
    @require_db
    def dbo(self):
        """The DB Object corresponding to this Artist."""
        cmp = 'name' if self.mbid is None else 'mbid'
        query = db.query(
            self.config,
            models.Artist
        ).filter(getattr(models.Artist, cmp) == getattr(self, cmp))

        try:
            return query.one()
        except NoResultFound:
            raise NoDatabaseObjectException()

    @require_db
    def create(self, price, max_available):
        """Create a DB Object corresponding to this Artist."""
        self.dbo = models.Artist(
            mbid=self.mbid,
            name=self.name,
            price=price,
            max_available=max_available
        )
        emptyhistory = models.ArtistHistory(
            self.dbo,
            db.utcnow(),
            price,
            0,
            0
        )
        db.add(self.config, self.dbo)
        db.add(self.config, emptyhistory)

    @memoised_property
    @require_lastfm
    def lastfm_info(self):
        """The lastfm get_info data corresponding to this Artist."""

        try:
            mbid = self.mbid
            return lfm.Artist.get_info(lastfm.params(
                self.config,
                mbid=mbid
            ))
        except:
            try:
                return lfm.Artist.get_info(lastfm.params(
                    self.config,
                    artist=self.name,
                    autocorrect=1
                ))
            except AttributeError:
                raise AttributeError('lastfm_info')

    # Static Methods

    @staticmethod
    @require_lastfm
    def correct(config, name):
        correction = lfm.Artist.get_correction(lastfm.params(
            config,
            artist=name
        ))
        if 'status' in correction:
            if correction['status'] == 'ok':
                return None
            else:
                raise ValueError('Invalid response from last.fm API server!')
        else:
            return correction['correction']['artist']

    @staticmethod
    @require_lastfm
    def api_search(config, name, limit=5, page=1):
        results = lfm.Artist.search(lastfm.params(
            config,
            artist=name,
            limit=limit,
            page=page
        ))['artistmatches']

        if type(results) is dict:
            results = results['artist']
            if type(results) is list:
                pass
            elif type(results) is dict:
                results = [results]
        else:
            results = []

        return (partial_artist(config, a) for a in results)

    @staticmethod
    @require_lastfm
    def popular(config, limit=10):
        results = lfm.Chart.get_top_artists(lastfm.params(config, limit=limit))

        if type(results) is dict:
            results = results['artist']
            if type(results) is list:
                pass
            elif type(results) is dict:
                results = [results]
        else:
            results = []

        return (partial_artist(config, a) for a in results)

    @staticmethod
    @require_db
    def top(config, limit=10, after=None):
        q = db.query(config, models.Artist)
        q = q.order_by(models.Artist.price.desc()).limit(limit)
        return (Artist(config, dbo=a) for a in q)

    @staticmethod
    @require_db
    def most_traded(config, limit=10):
        q = db.query(config, models.Artist).join(models.Trade)
        q = q.filter(models.Trade.purchase == True)
        q = q.group_by(models.Trade.artist_id)
        q = q.order_by(func.count(models.Trade.id).desc())
        q = q.limit(limit)
        return (Artist(config, dbo=o) for o in q)

    # Object Interface

    max_available = db.dbo_property('max_available')
    price = db.dbo_property('price')
    last_playcount = db.dbo_property('last_playcount')
    last_listeners = db.dbo_property('last_listeners')
    last_closing_price = db.dbo_property('last_closing_price')

    @property
    @require_db
    def points(self):
        return self.history(count=1)[0].points

    @property
    @require_db
    def dividend(self):
        return self.history(count=1)[0].dividends

    @property
    @require_db
    def no_remaining(self):
        """Return the number of artists remaining to be sold. Read-only."""
        return self.dbo.no_remaining

    @require_db
    def history(self, after=None, step=None, count=None):
        q = db.query(self.config, models.ArtistHistory).join(models.Artist)
        if after is not None:
            q = q.filter(models.ArtistHistory.date >= after)
        q = q.order_by(models.ArtistHistory.date.desc()).limit(count)

        return q.all()

    @memoised_property
    @require_lastfm
    def images(self):
        return {i['size']: i['#text'] for i in self.lastfm_info['image']}

    @property
    @require_lastfm
    def listeners(self):
        return int(self.lastfm_info['stats']['listeners'])

    @property
    @require_lastfm
    def playcount(self):
        return int(self.lastfm_info['stats']['playcount'])

    @property
    @require_lastfm
    def plays(self):
        return self.playcount

    @property
    @require_lastfm
    def bio(self):
        return self.lastfm_info['bio']

    @memoised_property
    @require_lastfm
    def similar(self):
        return (partial_artist(self.config, i)
            for i in self.lastfm_info['similar']['artist'])

    @memoised_property
    @require_lastfm
    def streamable(self):
        return self.lastfm_info['streamable'] == 1

def partial_artist(config, partial_info):
    return Artist(
        config,
        lastfm_info=PartialDict(
            partial_info,
            populator=partial(
                lfm.Artist.get_info,
                lastfm.params(
                    config,
                    artist=partial_info['name']
                )
            )
        )
    )

class ArtistNeedsMBIDException(lfm.lastfm.DataError):
    message = 'We don\'t deal in artists with no MBID!'

class NoStockRemainingException(Exception):
    pass
