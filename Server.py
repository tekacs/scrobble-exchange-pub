# Python Server

import sys
sys.path.append('gen-py')

from se_api import ScrobbleExchange
from se_api.ttypes import *
from se_api.constants import *

from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
from thrift.server import TServer

from functools import wraps as _wraps

import datm
import config

from datetime import datetime
import time, hmac

lastfm_config = {
    'api_key': config.lastfmcred['api_key'],
    'api_secret' : config.lastfmcred['secret']
}

db_args = {
    'url': 'sqlite:///db',
    'pool_size': None,
    'max_overflow': None
}

from functools import wraps as _wraps

def rethrow(f):
    exceptions = {
        datm.TransientError: TransientError,
        datm.AuthenticationError: AuthenticationError,
        datm.DataError: DataError,
        datm.ProgrammingError: ProgrammingError,
        datm.ServiceError: ServiceError
    }
    @_wraps(f)
    def inner(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except tuple(exceptions.keys()) as e:
            raise exceptions[e](e.message)
    
    return inner

class SEHandler(object):
    _config = datm.DATMConfig(lastfm=lastfm_config, db_args=db_args)
    
    def apikey(self):
        """
        Returns the SE API key for sending to last.fm
        """
        return config.lastfmcred['api_key']
    
    @rethrow
    def login(self, token):
        """
        If successful, returns the AuthUser with the user session token
        
        Parameters:
        - token
        """
        with datm.DATMSession(self._config):
            try:
                user = datm.user(self._config)
                sessiontoken = user.getSession(self._config, token)
                
                ret = AuthUser(name=User(name=user.name), 
                                                    session_key=sessiontoken)
                return ret
            except datm.InvalidAuthorisationException:
                raise AuthenticationError('User not authenticated')
    
    @rethrow
    def getArtist(self, artist):
        """
        Returns basic artist info. If either the artist or the mbid is unknown,
        then the empty string should be sent.
        
        Parameters:
        - artist
        """
        with datm.DATMSession(self._config):
            if not artist.mbid:
                a = datm.artist(self._config, mbid=artist.mbid)
            elif not artist.name:
                a = datm.artist(self._config, name=artist.name)
            else:
                raise DataError('Incorrect artist data')
                
            ret = Artist(mbid=a.mbid, name=a.name, imgurls=a.images)
        
            return ret
    
    @rethrow
    def getLightArtist(self, artist):
        """
        Returns only MBID and name. If either artist or mbid are unknown, 
        then the empty string should be sent
        
        Parameters:
        - artist
        """
        with datm.DATMSession(self._config):
            if not artist.mbid:
                a = datm.artist(self._config, mbid=artist.mbid)
            elif not artist.name:
                a = datm.artist(self._config, name=artist.name)
            else:
                raise DataError('Incorrect artist data')
            
            ret = Artist(mbid = a.mbid, name=a.name)
        
            return ret
    
    @rethrow
    def getArtistSE(self, artist, user):
        """
        Returns the data from our db. If the artist isn't there, the data 
        gets on-demand pulled. If either artist or mbid are unknown, then the 
        empty string should be sent. User sets the `ownedby' bool, by default it
        should be an empty string
        
        Parameters:
        - artist
        - user
        """
        with datm.DATMSession(self._config):
            if not artist.mbid:
                a = datm.artist(self._config, mbid=artist.mbid, user=user)
            elif not artist.name:
                a = datm.artist(self._config, name=artist.name, user=user)
            else:
                raise DataError('Incorrect artist data')
            
            u = datm.user(self._config, user.name)
            
            r = Artist(mbid=a.mbid, name=a.name, imgurls=a.images)
            
            
            try:
                ret = ArtistSE(artist=r, numremaining=a.no_remaining, 
                               points=a.points, dividend=a.dividend, 
                               ownedby=u.owns(a))
            except NoDatabaseObjectException():
                #a.create(mechanics.no_remaining, mechanics.points, 
                #mechanics.price, mechanics.dividend)
                #ret = ArtistSE(artist=r, numremaining=a.no_remaining, 
                #               points=a.points, dividend=a.dividend, 
                #               ownedby=u.owns(a))
                pass
            
            if (u.owns(a)):
                ret.price = int(a.price * 0.97)
            else:
                ret.price = a.price
            
            return ret
    
    @rethrow
    def getArtistLFM(self, artist, user):
        """
        Returns the artist info from last.fm for the artist. If either artist
        or mbid are unknown, then the empty string should be sent. An
        authenticated user is required to return recommended artists, otherwise
        the parameter should be set to none

        Parameters:
        - artist
        - user
        """
        with datm.DATMSession(self._config):
            if not artist.mbid:
                a = datm.artist(self._config, mbid=artist.mbid,
                                                session_key = user.session_key)
            elif not artist.name:
                a = datm.artist(self._config, name=artist.name,
                                                session_key = user.session_key)
            else:
                raise DataError('Incorrect artist data')

            b = ArtistBio(summary=a.summary, content=a.content)       
           
            r = Artist(mbid=a.mbid, name=a.name, imgurls=a.images)
            ret = ArtistLFM(artist=r, streamable=a.streamable,
                            listeners=a.listeners, plays=a.plays,
                            tags=a.tags, similar = a.similar, bio=b)
            
            return ret
    
    @rethrow
    def getArtistHistory(self, artist, n):
        """
        Returns a list of tuples of the price of the artist the past n days.
        For new artists the empty list is returned.
        
        Parameters:
        - artist
        - n
        """
        with datm.DATMSession(self._config):
            if not artist.mbid:
                a = datm.artist(self._config, mbid=artist.mbid)
            elif not artist.name:
                a = datm.artist(self._config, name=artist.name)
            else:
                raise DataError('Incorrect artist data')
            
            time_utc = time.mktime(datetime.utcnow().timetuple())
            time_utc_old = time_utc - n*24*60*60
            
            ret = ArtistHistory()
            try:
                ret.histvalue = a.history(self._config, after=time_utc_old)
            except NoDatabaseObjectException():
                #a.create(mechanics.no_remaining, mechanics.points, 
                #mechanics.price, mechanics.dividend)
                #ret.histvalue = a.history(self._config, after=time_utc_old)
                pass
            
            return ret
    
    @rethrow
    def searchArtist(self, text, n, page):
        """
        Returns a list of tuples of the price of the artist the past n days.
        For new artists the empty list is returned.

        Parameters:
        - artist
        - n
        """
        with datm.DATMSession(self._config):
            alist = datm.artist.search(self._config, text, limit=n, page=page)
            
            ret = [Artist(mbid=a.mbid, name=a.name, imgurls=a.images) for
                                                                    a in alist]
            
            return ret
    
    @rethrow
    def getSETop(self, n, trange):
        """
        Returns a list of the n top SE artists by decreasing value. Range is
        the number of days the leaderboard is over

        Parameters:
        - n
        - trange
        """
        with datm.DATMSession(self._config):
            
            time_utc = time.mktime(datetime.utcnow().timetuple())
            time_utc_old = time_utc - trange*24*60*60
            
            alist = datm.artist.top(self._config, limit=n, after=time_utc_old)
            
            ret = [Artist(mbid=a.mbid, name=a.name, imgurls=a.images) for
                                                                    a in alist]

            return ret
    
    @rethrow
    def getLFMTop(self, n):
        """
        Returns a list of the n top last.fm artists by decreasing value.

        Parameters:
        - n
        - trange
        """
        with datm.DATMSession(self._config):
            
            alist = datm.artist.popular(self._config, limit=n)
            
            ret = [Artist(mbid=a.mbid, name=a.name, imgurls=a.images) for
                                                                    a in alist]
            
            return ret
    
    @rethrow
    def getTradedArtists(self, n):
        """
        Returns a list of the n most traded artists by decreasing value.

        Parameters:
        - n
        """
        with datm.DATMSession(self._config):
            alist = datm.artist.most_traded(self._config, limit=n)
            
            ret = [Artist(mbid=a.mbid, name=a.name, imgurls=a.images) for
                                                                    a in alist]

            return ret
    
    @rethrow 
    def getRecentTrades(self, n):
        """
        Returns a list of the n most recent trades

        Parameters:
        - n
        """
        with datm.DATMSession(self._config):
            tlist = datm.trade.recent(self._config, limit=n)
            
            ret = [Artist(mbid=t.mbid, name=t.name, imgurls=t.images) for
                                                                    t in tlist]
            
            return ret
    
    @rethrow
    def getUserData(self, user):
        """
        Returns extended user data for the current user.
        
        Parameters:
        - user
        """
        with datm.DATMSession(self._config):
            u = datm.user(self._config, user)
            
            basicu = User(name=u.name, points=u.points)
            
            ret = UserData(user=basicu)
            ret.trades = []
            ret.stocks = []
            ret.trophies = [Trophy(name=u.trophies.name,
                                   description=u.trophies.description)]
            ret.league = League(name=u.league.name,
                                description=u.league.description,
                                icon=u.league.icon)
            
            for t in u.trades:
                a = Artist(mbid=t.Artist.mbid, name=t.Artist.name,
                           imgurls=t.Artist.images)
                
                ret.trades.append(Trade(artist=a, price=t.price, time=t.time))
            
            for t in u.stocks:
                a = Artist(mbid=t.Artist.mbid, name=t.Artist.name,
                           imgurls=t.Artist.images)
                
                #the assumption is that if the stock is listed, then it exists 
                #in the DB and no databaseobjectexception would be thrown
                ret.stocks.append(ArtistSE(artist=a, price=t.price, 
                                dividend=t.dividend, numremaining=no_remaining))
            
            return ret
        
    def getUserMoney(self, user):
        """
        Returns the current user with money. Requires AuthUser to auth
        
        Parameters:
        - user
        """
        with datm.DATMSession(self._config):
            u = datm.user(self._config, user.name, user.session_key)
            
            return AuthUser(name=User(name=user.name, points=u.points, 
                                session_key=user.session_key, money=u.money))

    def getTopUsers(self, n, league, trange):
        """
        Returns the n top users by decreasing value in the given league. Trange 
        is the number of days the leaderboard is over, rounded to the nearest 
        day, week or month.

        Parameters:
        - n
        - league
        - trange
        """
        with datm.DATMSession(self._config):
            
            if trange == 1:
                ulist = datm.user.top(self._config, limit=n, league=league.name,
                                        period='daily')
            elif trange <= 7:
                ulist = datm.user.top(self._config, limit=n, league=league.name,
                                        period='weekly')
            elif trange <= 31:
                ulist = datm.user.top(self._config, limit=n, league=league.name,
                                        period='monthly')
            else:
                raise DataError('Unusual time range selected')
            
            return UserLeaderboard(users=[User(name=u.name) for u in ulist])

    def getNearUsers(self, user):
        """
        Returns a list of 10 users with 4 above and 5 below in the leaderboard
        compared to the user provided, including the user's position.

        Parameters:
        - user
        """
        with datm.DATMSession(self._config):
            ulist = datm.user.near(self._config, name=user)
            
            return UserLeaderboard(users=[User(name=u.name) for u in ulist])
   
    def getGuarantee(self, artist, user):
        """
        Returns the guarantee token (elephant) to the front end
        
        Parameters:
        - artist
        - user
        """
        with datm.DATMSession(self._config):
            if not artist.mbid:
                a = datm.artist(self._config, mbid=artist.mbid, user=user)
            elif not artist.name:
                a = datm.artist(self._config, name=artist.name, user=user)
            else:
                raise DataError('Incorrect artist data')
            
            u = datm.user(self._config, user.name)
            
            if (u.owns(a)):
                price = int(a.price * 0.97)
            else:
                price = a.price
           
            # Calculating the elephant
            time_utc = time.mktime(datetime.utcnow().timetuple())

            m = hmac.new(datm.auth.secret(self._config))
            m.update(str(time_utc))
            m.update(str(price))
            el = m.hexdigest()
            
            return Guarantee(elephant = el, artist = Artist(mbid=a.mbid, 
                            name=a.name, imgurls=a.images), price=price,   
                            time=time_utc)
        

    def buy(self, guarantee, user):
        """
        Buys artist for user, and returns a bool as to whether it was
        successful or not

        Parameters:
        - guarantee
        - user
        """
        with datm.DATMSession(self._config):
            
            # Calculating the elephant
            time_utc = time.mktime(datetime.utcnow().timetuple())

            m = hmac.new(datm.auth.secret(self._config))
            m.update(str(time_utc))
            m.update(str(guarantee.price))
            el = m.hexdigest() 
            
            #authenticate the elephant
            if guarantee.elephant != el:
                raise DataError('Incorrect elephant')
            
            #check for 15s time (with some leeway)
            if (time_utc - guarantee.time) > 17:
                raise TransientError('Too late')
            
            u = datm.user(self._config, user=user.name)
            a = datm.artist(self._config, mbid=guarantee.artist.mbid)
            
            try:
                t = datm.trade(self._config, user=u, artist=a, 
price=guarantee.price)
                t.buy()
            except NoStockRemainingException:
                raise TransientError('No stock remaining')
        

    def sell(self, guarantee, user):
        """
        Sells artist for user, and returns a bool as to whether it was
        successful or not

        Parameters:
        - guarantee
        - user
        """
        with datm.DATMSession(self._config):
            
            # Calculating the elephant
            time_utc = time.mktime(datetime.utcnow().timetuple())

            m = hmac.new(datm.auth.secret(self._config))
            m.update(str(time_utc))
            m.update(str(guarantee.price))
            el = m.hexdigest() 
            
            #authenticate the elephant
            if guarantee.elephant != el:
                raise DataError('Incorrect Elephant')
            
            #check for 15s time (with some leeway)
            if (time_utc - guarantee.time) > 17:
                raise TransientError('Too late')
            
            u = datm.user(self._config, user=user.name)
            a = datm.artist(self._config, mbid=guarantee.artist.mbid)
            
            try:
                t = datm.trade(self._config, user=u, artist=a, 
price=guarantee.price)
                t.sell()
            except StockNotOwnedException:
                raise TransientError('User cannot sell')

#Create the databases
SEHandler._config.db.create_all()

processor = ScrobbleExchange.Processor(SEHandler())
transport = TSocket.TServerSocket(port=9090)
tfactory = TTransport.TBufferedTransportFactory()
pfactory = TBinaryProtocol.TBinaryProtocolFactory()

server = TServer.TThreadPoolServer(processor, transport, tfactory, pfactory)

print 'Starting the server...'
server.serve()
print 'done.'
