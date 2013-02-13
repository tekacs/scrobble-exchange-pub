"""Base (meta)classes for objects in DATM."""

__author__ = 'amar'

from functools import wraps

class DATMObject(object):
    @property
    def lastfm_object(self):
        return getattr(self, '_lastfm_object', None)

    @lastfm_object.setter
    def lastfm_object(self, value):
        setattr(self, '_lastfm_object', value)

    @property
    def db_object(self):
        return getattr(self, '_db_object', None)

    @db_object.setter
    def db_object(self, value):
        setattr(self, '_db_object', value)

def datm_setup(init):
    @wraps(init)
    def inner(self, config, *args, **kwargs):
        self._config = config
        self._session = config.session
        return init(self, config, *args, **kwargs)
    return init

class UserIsLyingToYouException(Exception):
    """Exceptions where the user is falsely representing itself to the API."""
    pass