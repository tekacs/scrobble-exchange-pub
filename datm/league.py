__author__ = 'amar'

from sqlalchemy.orm.exc import NoResultFound

import models

from util import db
from base import DATMObject, datm_setup, NoDatabaseObjectException
from config import require_db
from util.magic import memoised_property

class League(DATMObject):
    @datm_setup
    def __init__(self,
                 config,
                 uid=None,
                 name=None,
                 icon=None,
                 description=None,
                 dbo=None):
        if dbo is not None:
            self.dbo = dbo
        else:
            self.uid = uid
        if any((name, icon, description)):
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
            ).filter(models.League.uid == self.uid).one()
        except NoResultFound:
            raise NoDatabaseObjectException()

    @require_db
    def create(self):
        self.dbo = models.League(
            uid=self.uid,
            name=self.name,
            icon=self.icon,
            description=self.description
        )
        self.session.db.add(self.dbo)

    # Static methods

    @staticmethod
    @require_db
    def all(config):
        query = db.query(config, models.League).distinct()
        return (League(config, dbo=o) for o in query.all())

    # Object interface

    uid = db.dbo_property('uid')
    name = db.dbo_property('name')
    description = db.dbo_property('description')
    icon = db.dbo_property('icon')

    @property
    @require_db
    def users(self):
        return self.dbo.users