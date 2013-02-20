__author__ = 'amar'

import models

from util import db
from base import DATMObject
from config import require_data_source, require_lastfm, require_db

class Auth(DATMObject):
    @staticmethod
    @require_db
    def secret(config):
        db.query(config, models.Internal.secret).one().secret