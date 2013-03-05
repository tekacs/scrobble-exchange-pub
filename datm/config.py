__author__ = 'amar'

from functools import wraps

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import lfm
from models.base import Base as DeclarativeBase

import pdb # temp

class DATMConfig(object):
    def __init__(self,
                 lastfm=None,
                 db_args=None,
                 inner_config=None,
                 session=None,
                 debug=False):

        _db_args = {'pool_size': 20, 'max_overflow': 0}

        if  inner_config is not None:
            self._db = inner_config.db
            self._lastfm = inner_config.lastfm
            self._session = session
            return

        if lastfm is not None:
            try:
                request_builder = lfm.RequestBuilder(
                    api_key=lastfm['api_key'],
                    api_secret=lastfm['api_secret'],
                    debug=debug
                )
            except KeyError:
                raise TypeError(
                    'Argument lastfm must bear keys api_key, api_secret.'
                )
            self._lastfm = DATMLastFM(request_builder)

        if db_args is not None:
            _db_args.update(db_args)
            for key in [k for k, v in _db_args.iteritems() if v is None]:
                _db_args.pop(key)
            url = _db_args.pop('url')
            _db_args['echo'] = debug

            engine = create_engine(url, **_db_args)
            SessionBase = sessionmaker(bind=engine)
            self._db = DATMDatabase(engine, SessionBase)

    def clone(self, session=None):
        return DATMConfig(inner_config=self, session=session)

    @property
    def lastfm(self):
        return getattr(self, '_lastfm', None)

    @property
    def db(self):
        return getattr(self, '_db', None)

    @property
    def session(self):
        return self._session

class DATMLastFM(object):
    def __init__(self, request_builder):
        self._request_builder = request_builder

    @property
    def request_builder(self):
        return self._request_builder

    @property
    def rb(self):
        return self._request_builder

class DATMDatabase(object):
    def __init__(self, engine, SessionBase):
        self._engine = engine
        self._SessionBase = SessionBase

    @property
    def engine(self):
        return self._engine

    @property
    def SessionBase(self):
        return self._SessionBase

    def create_all(self):
        DeclarativeBase.metadata.create_all(self._engine)

def has_db(obj):
    return obj.db is not None

def has_lastfm(obj):
    return obj.lastfm is not None

def require_data_source(f):
    @wraps(f)
    def inner(first, *args, **kwargs):
        if has_db(first) or has_lastfm(first):
            return f(first, *args, **kwargs)
        else:
            raise NoDataSourceException(f.func_name)
    return inner

def require_lastfm(f):
    @wraps(f)
    def inner(first, *args, **kwargs):
        if not has_lastfm(first):
            raise NoLastFMException(f.func_name)
        return f(first, *args, **kwargs)
    return inner

def require_db(f):
    @wraps(f)
    def inner(first, *args, **kwargs):
        if not has_db(first):
            raise NoDatabaseException(f.func_name)
        return f(first, *args, **kwargs)
    return inner

class NoDataSourceException(Exception):
    """Base for exceptions for insufficiently diverse data sources."""
    message = "Insufficiently diverse data sources to perform that operation!"

class NoLastFMException(Exception):
    message = "Can't perform that operation without access to the last.fm API!"

class NoDatabaseException(Exception):
    message = "Can't perform that operation without access to the SE database!"