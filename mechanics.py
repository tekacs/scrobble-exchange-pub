import math

from datm import User, Artist

class User(object):
    def __init__(self, config, user):
        self.config = config
        self.user = user
    
    @property
    def initial_price(self):
        listeners = self.user.listeners
        playcount = self.user.playcount
        return (listeners + playcount)**(2.718281828)
    
    @property
    def initial_money(self):
        return 20000
    
    @property
    def initial_points(self):
        return 0

class Artist(object):
    def __init__(self, config, artist):
        self.config = config
        self.artist = artist
    
    @classmethod
    def no_players(cls, config):
        if getattr(cls, '_no_players', None) is None:
            cls._no_players = User.count(config)
        return cls._no_players
    
    @classmethod
    def listener_ratio(cls, config, listeners):
        if getattr(cls, '_max_listeners', None) is None:
            cls._max_listeners = Artist.max_listeners
        return listeners / cls._max_listeners
    
    @property
    def max_shares(self):
        return math.ceil(0.1 * self.no_players * self.listener_ratio(self.config, self.artist.listeners))