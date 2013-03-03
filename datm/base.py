"""Base (meta)classes for objects in DATM."""

__author__ = 'amar'

from functools import wraps

class DATMObject(object):
    @property
    def config(self):
        return self._config

    @property
    def session(self):
        return self._session

    @property
    def db(self):
        """Return the most specific db object available.

        The exception approach catches missing ``_session``s as well as missing
        ``db``s.
        """
        return self._config.db

    @property
    def lastfm(self):
        """Return the most specific lastfm object available.

        The exception approach catches missing ``_session``s as well as missing
        ``lastfm``s.
        """
        return self._config.lastfm

    @property
    def persisted(self):
        """Check if a database object exists corresponding to this object."""
        try:
            if self.dbo is not None:
                return True
        except NoDatabaseObjectException:
            return False

def datm_setup(init):
    @wraps(init)
    def inner(self, config, *args, **kwargs):
        self._config = config
        self._session = config.session
        return init(self, config, *args, **kwargs)
    return inner

class NoDatabaseObjectException(Exception):
    """The database object corresponding to the requested instance does not exist."""
    message = "The database object corresponding to the requested instance does not exist."

class UserIsLyingToYouException(Exception):
    """Exceptions where the user is falsely representing itself to the API."""