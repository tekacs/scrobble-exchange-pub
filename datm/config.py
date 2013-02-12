__author__ = 'amar'

from functools import wraps

from lastfm import Api
from sqlalchemy import create_engine

class DATMConfig(object):
    def __init__(self, lastfm=None, db=None):
        _db_args = {'pool_size': 20, 'max_overflow': 0}
        _lastfm = {}
        if lastfm is not None:
            try:
                api = Api(api_key=_lastfm['api_key'],
                            secret=_lastfm['secret'],
                            input_encoding='utf-8')
            except KeyError:
                raise TypeError(
                    'Argument lastfm must bear keys api_key, secret.'
                )
            self._lastfm = DATMLastFm(api)
        if db_args is not None:
            _db_args.update(db_args)
            url = _db_args.pop('url')
            engine = create_engine(url, **_db_args)
            self._db = DATMDatabase(engine)

    @property
    def lastfm(self):
        return self._lastfm

    @property
    def db(self):
        return self._db

class DATMLastFm(object):
    def __init__(self, api):
        self._api = api

    @property
    def api(self):
        return self._api

class DATMDatabase(object):
    def __init__(self, engine):
        self._engine = engine

    @property
    def engine(self):
        return self._engine

def require_data_source(f):
    @wraps(f)
    def inner(self, *args, **kwargs):
        if (self.lastfm is None) and (self.lastfm is None):
            raise NoDataSourceException()
        f(self, *args, **kwargs)
    return inner

def require_lastfm(f):
    @wraps(f)
    def inner(self, *args, **kwargs):
        if self.lastfm is None:
            raise NoLastFMException()
        f(self, *args, **kwargs)
    return inner

def require_db(f):
    @wraps(f)
    def inner(self, *args, **kwargs):
        if self.db is None:
            raise NoDatabaseException()
        f(self, *args, **kwargs)
    return inner

class NoDataSourceException(Exception):
    """Base for exceptions for insufficiently diverse data sources."""
    message = "Insufficiently diverse data sources to perform that operation!"
    pass

class NoLastFMException(Exception):
    message = "Can't perform that operation without access to the last.fm API!"
    pass

class NoDatabaseException(Exception):
    message = "Can't perform that operation without access to the SE database!"
    pass
