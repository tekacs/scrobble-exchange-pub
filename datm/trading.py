__author__ = 'amar'

from base import DATMObject, UserIsLyingToYouException
from config import require_data_source, require_lastfm, require_db

class Trade(DATMObject):
    def __init__(self, user, artist, price):
        pass

    @staticmethod
    @require_db
    def recent(self):
        pass

class NoStockRemainingException(Exception):
    pass

class StockNotOwnedException(UserIsLyingToYouException):
    pass