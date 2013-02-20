__author__ = 'amar'

from sqlalchemy.ext.declarative.api import DeclarativeMeta
from sqlalchemy.orm.attributes import InstrumentedAttribute

def query(config, *args, **kwargs):
    return config.session.db.query(*args, **kwargs)

def add(config, *args, **kwargs):
    return config.session.db.add(*args, **kwargs)

def abs_name(obj):
    if isinstance(obj, InstrumentedAttribute):
        return str(obj.__clause_element__())
    elif isinstance(obj, DeclarativeMeta):
        return obj.__tablename__
    raise NotImplementedError("I don't know what to do with that!")