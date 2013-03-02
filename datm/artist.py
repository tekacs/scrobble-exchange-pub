__author__ = 'amar'

from functools import partial

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
            self.name = correction[0]
            self.mbid = correction[1] or self.mbid

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
        except (NoLastFMException, KeyError):
            pass

        # In theory @require_data_source should prevent this from occurring.
        raise AttributeError('Artist object instantiated without name source.')

    @memoised_property
    def mbid(self):
        """Return the MBID corresponding to this object.

        Recognising that a request for this property should never cause loops
        is tricky at best.

        - Upon entering this method, both of its approaches to
        determining mbid ostensibly rely upon calls to this function itself!

        - Both methods try to query by mbid before doing a query by name and as
        such check this very property.

        - As such, this method sets self._mbid to None before making any such
        calls. This means that any requests for mbid whilst it is in the
        process of being determined will evaluate directly to None. This is to
        some extent a hack, and a thread-unsafe hack at that, but at least in
        principle, it should never *be* that two threads are directly addressing
        a single Artist instance.

        It should be noted that if the body of this method is being called then
        it cannot be that self._mbid was already set at the time of the method
        call and so no existing value need be stored for restoration.

        - Upon a successful return of the method, the wrapping decorator sets
        self._mbid to the returned value and all is right in the world again.

        - Upon a failed call, self._mbid is deleted.

        This should all only ever be a concern if this method is called solely
        with a name (no mbid, no pre-populated dbo or lastfm_info).
        """
        self._mbid = None

        try:
            return self.lastfm_info['mbid']
        except (NoLastFMException, KeyError):
            pass
        try:
            return self.dbo.mbid
        except (NoDatabaseException, NoDatabaseObjectException):
            pass

        del self._mbid

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
        self.session.add(self.dbo)

    @property
    @require_db
    def persisted(self):
        """Check if a database object exists corresponding to this artist."""
        try:
            if self.dbo is not None:
                return True
        except NoDatabaseObjectException:
            return False

    @memoised_property
    @require_lastfm
    def lastfm_info(self):
        """The lastfm get_info data corresponding to this Artist."""
        # FIXME: Underscore hack.
        if self._mbid is not None:
            return lfm.Artist.get_info(lastfm.params(
                self.config,
                mbid=self._mbid
            ))
        else:
            return lfm.Artist.get_info(lastfm.params(
                self.config,
                artist=self._name,
                autocorrect=1
            ))

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
                return name, None
            else:
                raise ValueError('Invalid response from last.fm API server!')
        else:
            correction = correction['correction']['artist']
            return correction['name'], correction['mbid']

    @staticmethod
    @require_lastfm
    def api_search(config, name, limit=5, page=1):
        results = lfm.Artist.search(lastfm.params(
            config,
            artist=name,
            limit=limit,
            page=page
        ))['artistmatches']['artist']
        return (partial_artist(config, a) for a in results)

    @staticmethod
    @require_lastfm
    def popular(config, limit=10):
        top_artists = lfm.Chart.get_top_artists(lastfm.params(config))['artist']
        return (partial_artist(config, a) for a in top_artists)

    @staticmethod
    @require_db
    def top(config, limit=10, after=None):
        query = db.query(models.Artist).order_by(
            models.Artist.points.desc()
        ).limit(limit)
        return (Artist(dbo=a) for a in query.all())

    @staticmethod
    @require_db
    def most_traded(limit=10):
        # TODO: this! (group by & func.count)
        pass

    # Object Interface

    max_available = db.dbo_property('max_available')
    price = db.dbo_property('price')

    @property
    @require_db
    def points(self):
        return self.history[0].points

    @property
    @require_db
    def no_remaining(self):
        """Return the number of artists remaining to be sold. Read-only."""
        return self.dbo.no_remaining

    @require_db
    def history(self, after, step=None):
        # FIXME: There has *got* to be a way to fetch FKs with a limit. :/
        history = self.dbo.history
        for i in history:
            if i.date >= after:
                yield i
            else:
                raise StopIteration()

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
    def plays(self):
        return int(self.lastfm_info['stats']['playcount'])

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

class NoStockRemainingException(Exception):
    pass