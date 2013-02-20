__author__ = 'amar'

from config import require_db

class Trophy(object):
    def __init__(self, name, description=None, icon=None):
        pass

    @property
    def name(self):
        return self._name

    @property
    @require_db
    def description(self):
        return self._desc

    @property
    @require_db
    def icon(self):
        return self._icon