__author__ = 'amar'

import thread

from config import NoDatabaseException, DATMDatabase

class DATMSession(object):
    def __init__(self, config):
        self._config = config
        if not isinstance(config, DATMDatabase):
            raise NoDatabaseException()
        self._db_session = config.db.SessionBase()

    def __enter__(self):
        self._config.sessions.current_session = self

    def __exit__(self):
        try:
            del self._config.sessions.current_session
        except TypeError:
            raise InvalidSessionException()
        self.db_session.commit()
        self.db_session.remove()

    @property
    def config(self):
        return self._config

    @property
    def db_session(self):
        return self._db_session

class InvalidSessionException(Exception):
    pass