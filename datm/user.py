__author__ = 'amar'

from sqlalchemy import func

import models

from util import db
from base import DATMObject, datm_setup
from config import require_data_source, require_lastfm, require_db

class User(DATMObject):
    """A last.fm and SE combined user."""

    @datm_setup
    def __init__(self, config, name, session_key=None):
        self._name = name

        if config.lastfm is not None:
            self.lastfm_object = config.lastfm.api.get_user(name)

        if config.db is not None:
            self.db_object = db.query(config, models.User).filter(models.User.name == name).first()

    @property
    @staticmethod
    def count(config):
        """The number of users currently registered."""
        db.query(config, func.count(User.id)).scalar()

    @property
    def name(self):
        """The username of the user."""
        return self._name

    def authenticate(self, key):
        """Validate a user's session key against the database and auth."""
        if self.db_object.session_key == key:
            self._data['session_key'] = key

    @property
    @require_lastfm
    def real_name(self):
        """The real-world name of the user."""
#        self.lastfm_object.

    @property
    @require_lastfm
    def image(self):
        """The URL to the this user's image."""
        pass

    @property
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
