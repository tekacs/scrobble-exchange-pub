__author__ = 'amar'

import models

from util import db
from base import DATMObject, datm_setup
from config import require_data_source, require_lastfm, require_db

class Auth(DATMObject):
    @datm_setup
    def __init__(self, config):
        """datm_setup does everything necessary for this constructor."""
        pass # Unneeded, but pretty. :)

    @property
    @require_db
    def secret(self):
        return db.query(self.config, models.Internal.secret).one().secret

    @secret.setter
    @require_db
    def secret(self, value):
        m = db.query(self.config, models.Internal.secret).one()
        m.secret = value

    @property
    @require_db
    def destroy(self):
        q = db.query(self.config, models.Internal)
        db.delete(self.config, q.one())

    @require_db
    def create(self, secret):
        o = models.Internal(secret=secret)
        db.add(self.config, o)