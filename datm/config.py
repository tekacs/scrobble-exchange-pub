__author__ = 'amar'

# FIXME: Shouldn't need to munge sys.path! :P
import sys
sys.path.append('..')

import threading
from functools import wraps

from lastfm import Api
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from base import DATMObject

class DATMConfig(object):
    def __init__(self, lastfm=None, db_args=None):
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
            SessionBase = sessionmaker(bind=engine)
            self._db = DATMDatabase(engine, SessionBase)
        self._sessions = threading.local()

    @property
    def lastfm(self):
        getattr(self, '_lastfm', None)

    @property
    def db(self):
        getattr(self, '_db', None)

    @property
    def session(self):
        return self._sessions.current_session

class DATMLastFm(object):
    def __init__(self, api):
        self._api = api

    @property
    def api(self):
        return self._api

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

def has_db(obj):
    if isinstance(obj, DATMObject):
        return obj.db_object is not None
    if isinstance(obj, DATMConfig):
        return obj.session is not None
    return False

def has_lastfm(obj):
    if isinstance(obj, DATMObject):
        return obj.lastfm_object is not None
    if isinstance(obj, DATMConfig):
        return obj.lastfm is not None
    return False

def require_data_source(f):
    @wraps(f)
    def inner(first, *args, **kwargs):
        if has_db(first) or has_lastfm(first):
            return f(first, *args, **kwargs)
        else:
            raise NoDataSourceException()
    return inner

def require_lastfm(f):
    @wraps(f)
    def inner(first, *args, **kwargs):
        if not has_lastfm(first):
            raise NoLastFMException()
        return f(first, *args, **kwargs)
    return inner

def require_db(f):
    @wraps(f)
    def inner(first, *args, **kwargs):
        if has_db(first):
            raise NoDatabaseException()
        return f(first, *args, **kwargs)
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
