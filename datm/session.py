__author__ = 'amar'

import thread

from sqlalchemy.orm import sessionmaker

from config import NoDatabaseException

class DATMSession(object):
    def __init__(self, config):
        self._config = config
        if config.db is None:
            raise NoDatabaseException()
        self._db_session = sessionmaker(bind=config.db.engine)

    def __enter__(self):
        self._config.sessions[thread.get_ident()]

    def __exit__(self):
        try:
            self._config.sessions.popitem(thread.get_ident())
        except KeyError:
            raise InvalidSessionException()

class InvalidSessionException(Exception):
    pass