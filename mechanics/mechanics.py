# -*- coding: utf-8 -*-

from functools import partial
import decimal
D = decimal.Decimal
D.ceil = partial(D.to_integral, rounding=decimal.ROUND_UP)
D.round_even = partial(D.to_integral, rounding=decimal.ROUND_HALF_EVEN)

import datm

class User(object):
    def __init__(self, user):
        self.config = user.config
        self.user = user

    def daily(self):
        pass

    def reset(self):
        for artist in self.user.stocks:
            self.sell(artist)
        self.user.points = self.initial_points
        self.user.money = self.initial_money

    def buy(self, artist, price):
        if isinstance(artist, Artist):
            artist = artist.artist
        if self.user.owns(artist):
            raise ArtistAlreadyOwnedError()
        if self.user.money < price:
            raise NotEnoughMoneyError()
        if artist.no_remaining <= 0:
            raise NoStockRemainingException((artist.name, artist.max_available, artist.no_remaining))

        t = datm.Trade(self.config, user=self.user, artist=artist, price=price)
        t.create(purchase=True)

        self.user.money -= price

    def sell(self, artist, price):
        if isinstance(artist, Artist):
            artist = artist.artist
        if not self.user.owns(artist):
            raise ArtistNotOwnedError()

        t = datm.Trade(self.config, user=self.user, artist=artist, price=price)
        t.create(purchase=False)

        self.user.money += price

    @staticmethod
    def count(config):
        """Actively count the number of users in the database."""
        return datm.User.count(config)

    @property
    def initial_money(self):
        """This value is a constant."""
        return 20000
    
    @property
    def initial_points(self):
        """This value is a constant."""
        return 0

class Artist(object):
    def __init__(self, artist):
        self.config = artist.config
        self.artist = artist

    def daily(self):
        pass

    def price(self, owned=False):
        """Get current buy/sell price. Uses half-even rounding."""
        base = self.artist.price * (D(1) if owned else D('0.98'))
        return int(D.round_even(base))

    @property
    def score(self):
        """Daily Score = 0.0005 * ∆S + 0.05 * ∆L"""
        artist = self.artist
        listener_delta = artist.listeners - artist.last_listeners
        playcount_delta = artist.plays - artist.last_playcount
        base = (D('0.0005') * playcount_delta) + (D('0.05') * listener_delta)
        return int(D.round_even(base))

    @property
    def dividend(self):
        """Dividends = 0.01 * (3 * ∆√S + 0.05 * ∆L)"""
        artist = self.artist
        listener_delta = artist.listeners - artist.last_listeners
        playcount_delta = artist.plays - artist.last_playcount
        base = (3 * D(playcount_delta).sqrt()) + (D('0.05') * listener_delta)
        base = D('0.01') * base
        return int(D.round_even(base))

    @property
    def initial_price(self):
        """Initial Price = 0.07 * S / √L"""
        artist = self.artist
        base = D('0.07') * D(artist.plays) / D(artist.listeners).sqrt()
        return int(D.round_even(base))

    @property
    def max_shares(self):
        """Max. shares = ceil(0.1 * n * L / L_max)"""
        top = list(datm.Artist.popular(self.config, limit=1))[0]
        max_listeners = D(top.listeners)
        base = D(0.1) * User.count(self.config) * self.artist.listeners
        base = base / max_listeners
        return int(D.ceil(base))

class PurchaseError(Exception):
    pass

class ArtistAlreadyOwnedError(PurchaseError):
    message = "You can't buy an artist you already own!"

class ArtistNotOwnedError(PurchaseError):
    message = "You can't sell an artist you don't own!"

class NotEnoughMoneyError(PurchaseError):
    message = "You don't have enough money to make that purchase!"

class NoStockRemainingException(PurchaseError):
    message = "This artist is currently out of stock! You can try again later!"
