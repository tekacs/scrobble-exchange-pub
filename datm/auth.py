__author__ = 'amar'

import models

from util import db
from base import DATMObject, datm_setup
from config import require_data_source, require_lastfm, require_db

class Auth(DATMObject):
    @datm_setup
    def __init__(self, config):
        pass

    @property
    @require_db
    def secret(self):
        return db.query(self.config, models.Internal.secret).one().secret

    @secret.setter
    @require_db
    def secret(self, value):
        m = db.query(self.config, models.Internal.secret).one()
        m.secret = value
