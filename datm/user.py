__author__ = 'Amar Sood (tekacs)'

from sqlalchemy import func

import lfm
import models

from util import db, lastfm
from util.magic import memoised_property
from base import DATMObject, datm_setup
from config import require_lastfm, require_db

class User(DATMObject):
    """A last.fm and SE combined user."""

    @datm_setup
    def __init__(self, config, name, session_key=None):
        self._name = name

    @memoised_property
    @require_db
    def dbo(self):
        return db.query(
            self.config,
            models.User
        ).filter(models.User.name == self.name).one()

    @memoised_property
    @require_lastfm
    def lastfm_info(self):
        return lfm.User.get_info(lastfm.params(self.config, user=self.name))

    @memoised_property
    def name(self):
        """The username of the user."""
        return self._name

    @classmethod
    @require_db
    def count(config):
        """The number of users currently registered."""
        db.query(config, func.count(User.id)).scalar()

    @require_db
    def authenticate(self, key):
        """Validate a user's session key against the database and auth."""
        if self.dbo.session_key == key:
            self._data['session_key'] = key

    @memoised_property
    @require_lastfm
    def real_name(self):
        """The real-world name of the user."""
#        self.lastfm_object.

    @memoised_property
    @require_lastfm
    def image(self):
        """The URL to the this user's image."""
        pass

    @memoised_property
    @require_lastfm
    def subscriber(self):
        """Whether this user is a subscriber."""
        pass

    @property
    @require_db
    def money(self):
        """The amount currently available for this user to spend."""
        pass

    @property
    @require_db
    def owns(self, artist):
        """Determine whether a user owns a given artist."""
        pass

    @property
    @require_db
    def stocks(self):
        """Return all stocks owned by this user."""
        pass

    @property
    @require_db
    def trades(self, limit=None):
        """Return trades ever made by this user."""
        pass

    @property
    @require_db
    def trophies(self):
        """Return all trophies currently possessed by this user."""

class UserNotAuthenticatedException(Exception):
    """Raised upon an attempt to call an authenticated method sans auth."""
    pass

class InvalidAuthorisationException(Exception):
    """Raised upon an invalid attempt to authenticate."""
    pass
