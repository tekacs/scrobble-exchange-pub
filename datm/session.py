__author__ = 'amar'

from config import has_db, NoDatabaseException

class DATMSession(object):
    def __init__(self, config):
        self._config = config
        if has_db(config):
            self._db = config.db.SessionBase()

    def __enter__(self):
        self.bind()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            return False

        if self.db is not None:
            self.db.commit()

        self.unbind()

    def bind(self):
        self.config.sessions.current_session = self

    def unbind(self):
        try:
            del self.config.sessions.current_session
        except TypeError:
            raise InvalidSessionException()

    @property
    def config(self):
        return self._config

    @property
    def db(self):
        try:
            return self._db
        except AttributeError:
            raise NoDatabaseException()

class InvalidSessionException(Exception):
    pass