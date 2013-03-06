__author__ = 'Amar Sood (tekacs)'

from sqlalchemy import func
from sqlalchemy.orm.exc import NoResultFound

import lfm
import models

from util import db, lastfm
from util.magic import memoised_property, underscore_property
from lfm.lastfm import AuthenticationFailure
from base import DATMObject, datm_setup, NoDatabaseObjectException
from config import require_lastfm, require_db, require_data_source,\
    NoDatabaseException, NoLastFMException
from artist import Artist, partial_artist
from trading import Trade
from sparkles import Trophy
from league import League

class User(DATMObject):
    """A last.fm and SE combined user."""

    @datm_setup
    def __init__(self,
                 config,
                 name=None,
                 dbo=None,
                 lastfm_info=None):
        if lastfm_info is not None:
            self.lastfm_info = lastfm_info
        if dbo is not None:
            self.dbo = dbo
        if name is not None:
            self.name = name

    # Primary Key

    @memoised_property
    @require_data_source
    def name(self):
        """The user's name.

        This method body will not be executed in many cases as this value will
        be explicitly set upon construction of the class and this body bypassed.

        It doesn't require a data source as it is possible to have constructed
        an object with data but no data source (:/).
        """
        try:
            return self.dbo.name
        except (NoDatabaseException, NoDatabaseObjectException):
            pass
        try:
            return self.lastfm_info['name']
        except (NoLastFMException, KeyError):
            pass

        # In theory @require_data_source should prevent this from occurring.
        raise AttributeError('User object instantiated without name source.')

    # Data Accessors & Create

    @memoised_property
    @require_db
    def dbo(self):
        """The DB Object corresponding to this User."""
        query = db.query(
            self.config,
            models.User
        ).filter(models.User.name == self.name)

        try:
            return query.one()
        except NoResultFound:
            raise NoDatabaseObjectException()

    @require_db
    def create(self, money, points, league=None):
        """Create a new DB Object and prepare it to be saved."""
        self.dbo = models.User(name=self.name, money=money, points=points)
        self.dbo.league = league.dbo
        self.session.db.add(self.dbo)

    @memoised_property
    @require_lastfm
    def lastfm_info(self):
        """Get a get_info dictionary from last.fm. Memoised."""
        return lfm.User.get_info(lastfm.auth_params(
            self.config,
            user=self.name
        ))

    @require_lastfm
    @require_db
    def top_artists(self, limit=10):
        """Return the top artists from this user's last.fm Library"""
        lfm_data = lfm.User.get_top_artists(lastfm.auth_params(
            self.config,
            user=self.name,
            limit=limit
        ))
        if lfm_data.get('status', False) == 'ok':
            return []
        return (partial_artist(self.config, a) for a in lfm_data['artist'])

    # Static Methods

    @staticmethod
    @require_lastfm
    def getSession(config, token):
        try:
            return lfm.Auth.get_session(lastfm.auth_params(
                config,
                token=token
            ))
        except AuthenticationFailure as e:
            raise InvalidAuthorisationException(e.message)

    @staticmethod
    @require_db
    def count(config):
        """The number of users currently registered."""
        return db.query(config, func.count(models.User.id)).scalar()

    @staticmethod
    @require_db
    def top(config, limit=10, period=None, league=None):
        """Return the ``limit`` users with the most points over ``period``.

        period from options
        """
        query = db.query(config, models.User)

        if league is not None:
            query = query.filter(models.User.league == league.dbo)

        query = query.order_by(models.User.points_by_period(period).desc())
        query = query.limit(limit)

        return (User(config, dbo=u) for u in query)

    # Object Interface

    money = db.dbo_property('money')
    points = db.dbo_property('points')

    daily_points = db.dbo_property('daily_points')
    weekly_points = db.dbo_property('weekly_points')
    monthly_points = db.dbo_property('monthly_points')

    last_reset = db.dbo_property('last_reset')

    def points_by_period(self, period):
        options = (None, 'daily', 'weekly', 'monthly')
        if not period in options:
            raise ValueError('Period must be in %s' % (options,))
        period = (period or '') + ('' if period is None else '_')
        period += 'points'
        return getattr(self, period)

    @memoised_property
    def session_key(self):
        """This object's session_key."""
        return self.dbo.session_key

    @require_db
    def authenticate(self, key):
        """Validate a user's session key against the database and auth."""
        if self.dbo.session_key == key:
            self.session_key = key
        else:
            raise InvalidAuthorisationException()

    @require_db
    def vouch_for(self, session_key):
        self.dbo.session_key = session_key

    @require_db
    def owns(self, artist):
        """Determine whether a user owns a given artist."""
        return artist.dbo in self.dbo.artists

    @property
    @require_db
    def stocks(self):
        """Return stocks owned by this user."""
        return (Artist(self.config, dbo=o) for o in self.dbo.artists)

    @require_db
    def trades(self, limit=None):
        """Return trades ever made by this user."""
        return (Trade(self.config, dbo=o) for o in self.dbo.trades)

    @require_db
    def bought(self, artist):
        """Act on a vouched-for purchase of this artist by this user."""
        self.dbo.artists.append(artist.dbo)

    @require_db
    def sold(self, artist):
        """Act on a vouched-for sale of this artist by this user."""
        self.dbo.artists.remove(artist.dbo)

    @require_db
    def trophies(self, limit=None):
        """Return all trophies currently possessed by this user."""
        return (Trophy(self.config, dbo=o) for o in self.dbo.trophies)

    @require_db
    def add_trophy(self, trophy):
        """Add a Trophy to this user's trophies."""
        self.dbo.trophies.append(trophy.dbo)

    @property
    @require_db
    def league(self):
        o = self.dbo.league
        if o is None:
            raise NoDatabaseObjectException()
        return League(self.config, dbo=o)

    @require_db
    def rank(self, period):
        q = db.query(self.config, models.User)
        q = q.filter(models.User.league == self.league.dbo)
        q = q.filter(
            models.User.points_by_period(period) > self.points_by_period(period)
        )
        return q.count()

    @require_db
    def position(self, period):
        q = db.query(self.config, models.User)
        q = q.filter(models.User.league == self.league.dbo)
        q = q.filter(
            models.User.points_by_period(period) > self.points_by_period(period)
        )
        return q.group_by(models.User.points).count() + 1

    @require_db
    def near(self, up, down, period=None):
        q = db.query(self.config, models.User)
        q = q.filter(models.User.league == self.league.dbo)

        pos = self.rank(period)
        q = q.order_by(models.User.points_by_period(period).desc())
        return (User(self.config, dbo=u) for u in q.slice(pos - up, pos + down))

    @memoised_property
    @require_lastfm
    def tags(self):
        return self.lastfm_info['tags']

    @memoised_property
    @require_lastfm
    def images(self):
        """The URL to the this user's image."""
        return {i['size']: i['#text'] for i in self.lastfm_info['image']}

    @memoised_property
    @require_lastfm
    def real_name(self):
        """The real-world name of the user."""
        return self.lastfm_info['realname']

    @memoised_property
    @require_lastfm
    def subscriber(self):
        """Whether this user is a subscriber."""
        return self.lastfm_info['subscriber'] == 1

class UserNotAuthenticatedException(Exception):
    """Raised upon an attempt to call an authenticated method sans auth."""

class InvalidAuthorisationException(Exception):
    """Raised upon an invalid attempt to authenticate."""
