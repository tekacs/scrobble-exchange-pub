__author__ = 'amar'

import datetime

from sqlalchemy.ext.declarative.api import DeclarativeMeta
from sqlalchemy.orm.attributes import InstrumentedAttribute

# Watch out for circular imports with the below!
from ..base import NoDatabaseObjectException
from ..config import NoDatabaseException

def query(config, *args, **kwargs):
    return config.session.db.query(*args, **kwargs)

def add(config, *args, **kwargs):
    return config.session.db.add(*args, **kwargs)

def delete(config, *args, **kwargs):
    return config.session.db.delete(*args, **kwargs)

def dirty(config):
    return config.session.db.dirty

def commit(config):
    config.session.db.commit()

def refresh(config, dbo):
    config.session.db.refresh(dbo)

def db(config):
    return config.session.db

def utcnow():
    return int(datetime.datetime.utcnow().strftime("%s"))

def abs_name(obj):
    if isinstance(obj, InstrumentedAttribute):
        return str(obj.__clause_element__())
    elif isinstance(obj, DeclarativeMeta):
        return obj.__tablename__
    raise NotImplementedError("I don't know what to do with that!")

def dbo_property(name):
    """A property which passes through to dbo if it exists, else underscores.

    That is to say that it stores local state so long as no DB object exists
    but returns DB data if it is available.

    Chiefly useful for pre-filling attributes on a class and then creating or
    finding a database entry corresponding to it.

    Suggested flow:

        >>> User.name = 'test' # User._name = 'test'
        >>> User.dbo           # filter(m.User.name == User.name)
                                                  # == User._name == 'test'
        <User with name 'test'>
    """
    underscore = '_{}'.format(name)

    def failover(self):
        try:
            dbo = self.dbo
            if dbo is not None:
                return self.dbo, name
        except (NoDatabaseException, NoDatabaseObjectException):
            pass
        return self, underscore

    @property
    def prop(self):
        target = failover(self)
        try:
            return getattr(target[0], target[1])
        except AttributeError:
            raise NoDatabaseObjectException()
    @prop.setter
    def prop(self, value):
        target = failover(self)
        setattr(target[0], target[1], value)
    @prop.deleter
    def prop(self):
        """Delete only underscore/local attribute!

        Deleting on dbo is rather pointless. Set to None instead!
        """
        delattr(self, underscore)
    return prop