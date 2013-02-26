__author__ = 'amar'

import models

from util import db
from base import DATMObject, datm_setup
from config import require_db
from util.magic import memoised_property

class Trophy(DATMObject):
    @datm_setup
    def __init__(self, config, name, description=None, icon=None):
        self._name = name

    @memoised_property
    @require_db
    def dbo(self):
        return db.query(
            self.config,
            models.Trophy
        ).filter(models.Trophy.name == self.name).one()

    @property
    def name(self):
        return self._name

    @property
    @require_db
    def description(self):
        return self.dbo.desc

    @description.setter
    @require_db
    def description(self, value):
        self.dbo.desc = value

    @property
    @require_db
    def icon(self):
        return self.dbo.icon

    @icon.setter
    @require_db
    def icon(self, value):
        self.dbo.icon = value