__author__ = 'amar'

import datetime

from sqlalchemy.orm.exc import NoResultFound

import models
from util import db
from util.magic import memoised_property
from base import DATMObject, datm_setup,\
    NoDatabaseObjectException, UserIsLyingToYouException
from config import require_data_source, require_lastfm, require_db

class Trade(DATMObject):
    @datm_setup
    def __init__(self,
                 config,
                 id=None,
                 user=None,
                 artist=None,
                 price=None,
                 dbo=None):
        if dbo is not None:
            self.dbo = dbo
        elif id is not None:
            self.id = id
        else:
            self.user = user
            self.artist = artist
            self.price = price

    @memoised_property
    @require_db
    def id(self):
        dbo = self.dbo
        if self.dbo is None:
            raise NoDatabaseObjectException()
        return dbo.id

    @memoised_property
    @require_db
    def dbo(self):
        query = db.query(self.config, models.Trade).filter(
            models.Trade.id == self.id
        )
        try:
            return query.one()
        except NoResultFound:
            raise NoDatabaseObjectException()

    def create(self, purchase):
        self.dbo = models.Trade(
            user=self.user.dbo,
            artist=self.artist.dbo,
            price=self.price,
            purchase=purchase,
            date=int(datetime.datetime.utcnow().strftime("%s"))
        )
        self.session.db.add(self.dbo)

    user = db.dbo_property('user')
    artist = db.dbo_property('artist')
    price = db.dbo_property('price')
    date = db.dbo_property('date')

    @staticmethod
    @require_db
    def recent(config, limit=25):
        query = db.query(config, models.Trade).order_by(
            models.Trade.id.desc()
        ).limit(limit)
        return query.all()

class NoStockRemainingException(Exception):
    pass

class StockNotOwnedException(UserIsLyingToYouException):
    pass