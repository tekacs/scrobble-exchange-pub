__author__ = 'amar'

from sqlalchemy.orm.exc import NoResultFound

import models

from util import db
from util.magic import underscore_property
from base import DATMObject, datm_setup, NoDatabaseObjectException
from config import require_db
from util.magic import memoised_property

class League(DATMObject):
    @datm_setup
    def __init__(self,
                 config,
                 id=None,
                 name=None,
                 icon=None,
                 description=None,
                 dbo=None):
        if dbo is not None:
            self.dbo = dbo
        elif id is not None:
            self.id = id
        else:
            self.id = None
            self.name = name
            self.icon = icon
            self.description = description

    # Data Accessors & Create

    @memoised_property
    @require_db
    def dbo(self):
        try:
            return db.query(
                self.config,
                models.League
            ).filter(models.League.id == self.id).one()
        except NoResultFound:
            raise NoDatabaseObjectException()

    @require_db
    def create(self):
        self.dbo = models.League(self.name, self.icon, self.description)
        self.session.db.add(self.dbo)

    # Static methods

    @staticmethod
    @require_db
    def all(config):
        query = db.query(models.League).distinct()
        return (League(config, dbo=o) for o in query.all())

    # Object interface

    id = underscore_property('id')
    name = db.dbo_property('name')
    description = db.dbo_property('description')
    icon = db.dbo_property('icon')

    @property
    @require_db
    def users(self):
        return self.dbo.users