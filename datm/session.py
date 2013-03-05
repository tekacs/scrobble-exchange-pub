__author__ = 'amar'

from config import has_db

class DATMSession(object):
    def __init__(self, config):
        self._base_config = config
        self._config = config.clone(self)
        if has_db(config):
            self._db = config.db.SessionBase()

    def __enter__(self):
        self.bind()
        return self.config

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            return False

        if self.db is not None:
            self.db.commit()

        self.unbind()

    def bind(self):
        self._config = self.config.clone(self)
        return self.config

    def unbind(self):
        try:
            self._config = self._base_config
        except TypeError:
            raise InvalidSessionException()
        return self.config

    @property
    def config(self):
        return self._config

    @property
    def db(self):
        return self._db

class InvalidSessionException(Exception):
    pass