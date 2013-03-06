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
from mechanics import mechanics

from datetime import datetime
import time, hmac

lastfm_config = {
    'api_key': config.lastfmcred['api_key'],
    'api_secret' : config.lastfmcred['secret']
}

db_args = {
    #'url': 'postgresql://api:Koo4ahBa0chahz@localhost:5432/api'
    'url': 'sqlite:///db',
    'pool_size': None,
    'max_overflow': None
}

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
            for p in type(e).mro():
                if p in exceptions:
                    raise exceptions[p](e.message)
            raise e
    
    return inner

class SEHandler(object):
    _config = datm.DATMConfig(lastfm=lastfm_config, db_args=db_args, debug=True)
    _time_offset = 15
    
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
        with datm.DATMSession(self._config) as datmconfig:
            try:
                
                session = datm.User.getSession(datmconfig, token)
                
                user = datm.User(datmconfig, name=session['name'])
                
                if not user.persisted:
                    u = mechanics.User(user)
                    user.create(money=u.initial_money, points=u.initial_points, 
                                league=datm.League(datmconfig, uid='bronze'))
                    
                    ret = AuthUser(user=User(name=user.name), 
                                    session_key=session['key'], newuser=True)
                else:
                    ret = AuthUser(user=User(name=user.name), 
                                    session_key=session['key'], newuser=False)
                
                user.vouch_for(session['key'])
               
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
        with datm.DATMSession(self._config) as datmconfig:
            if artist.mbid:
                a = datm.Artist(datmconfig, mbid=artist.mbid)
            elif artist.name:
                a = datm.Artist(datmconfig, name=artist.name)
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
        with datm.DATMSession(self._config) as datmconfig:
            if artist.mbid:
                a = datm.Artist(datmconfig, mbid=artist.mbid)
            elif artist.name:
                a = datm.Artist(datmconfig, name=artist.name)
            else:
                raise DataError('Incorrect artist data')
            
            ret = Artist(mbid = a.mbid, name=a.name)
        
            return ret
    
    @rethrow
    def getArtistSE(self, artist, user):
        """
        Returns the data from our db. If the artist isn't there, the data 
        gets on-demand pulled. If either artist or mbid are unknown, then the 
        empty string should be sent. User sets the `ownedby' bool, by default 
        the user name should be an empty string
        
        Parameters:
        - artist
        - user
        """
        with datm.DATMSession(self._config) as datmconfig:
            if artist.mbid:
                a = datm.Artist(datmconfig, mbid=artist.mbid)
            elif artist.name:
                a = datm.Artist(datmconfig, name=artist.name)
            else:
                raise DataError('Incorrect artist data')
            
            r = Artist(mbid=a.mbid, name=a.name, imgurls=a.images)
            
            ma = mechanics.Artist(a)
            if not a.persisted:
                a.create(ma.initial_price, ma.max_shares)
            
            ret = ArtistSE(artist=r, numremaining=a.no_remaining, 
                               points=a.points, dividend=a.dividend)
            
            #Empty user sent, special case to mean anonymous
            if not user.name:
                ret.ownedby = False
                ret.price = a.price
            else:
                u = datm.User(datmconfig, user.name)
                ret.ownedby = u.owns(a)
                ret.price = ma.price(owned=ret.ownedby)
            
            return ret
    
    @rethrow
    def getArtistLFM(self, artist):
        """
        Returns the artist info from last.fm for the artist. If either artist
        or mbid are unknown, then the empty string should be sent.

        Parameters:
        - artist
        """
        with datm.DATMSession(self._config) as datmconfig:
            if artist.mbid:
                a = datm.Artist(datmconfig, mbid=artist.mbid)
            elif artist.name:
                a = datm.Artist(datmconfig, name=artist.name)
            else:
                raise DataError('Incorrect artist data')

            b = ArtistBio(summary=a.bio['summary'], content=a.bio['content'])  
           
            r = Artist(mbid=a.mbid, name=a.name, imgurls=a.images)
            ret = ArtistLFM(artist=r, streamable=a.streamable,
                            listeners=a.listeners, plays=a.plays,
                            tags=[], similar=[], bio=b)
            
            for sim in a.similar:
                if sim.mbid:
                    asim = Artist(mbid=sim.mbid, name=sim.name,
                                                            imgurls=sim.images)
                
                    ret.similar.append(asim)
            
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
        with datm.DATMSession(self._config) as datmconfig:
            if artist.mbid:
                a = datm.Artist(datmconfig, mbid=artist.mbid)
            elif artist.name:
                a = datm.Artist(datmconfig, name=artist.name)
            else:
                raise DataError('Incorrect artist data')
            
            time_utc = time.mktime(datetime.utcnow().timetuple())
            time_utc_old = int(time_utc - n*24*60*60)
            
            ret = ArtistHistory({},{},{})
            
            if not a.persisted:
                ma = mechanics.Artist(a)
                a.create(ma.initial_price, ma.max_shares)
            
            for h in a.history(after=time_utc_old):
                ret.histprice[h.date] = h.price
                ret.histpoints[h.date] = h.points
                ret.histdividends[h.date] = h.dividends
            
            return ret
    
    @rethrow
    def searchArtist(self, text, n, page):
        """
        returns a list of possible artists from a partial string. Ordered by 
        decreasing relevance. List size is limited to n elements, and page 
        returns the given page of results

        Parameters:
        - artist
        - n
        """
        with datm.DATMSession(self._config) as datmconfig:
            alist = datm.Artist.api_search(datmconfig, text, limit=n, page=page)

            ret = [Artist(mbid=a.mbid, name=a.name, imgurls=a.images) for a in 
                                                                alist if a.mbid]
            
            return ret
    
    @rethrow
    def getSETop(self, n, trange, user):
        """
        Returns a list of the n top SE artists by decreasing value. Trange is
        the number of days the leaderboard is over. User returns relevant 
        prices for each artist, otherwise buy price for anonymous users.

        Parameters:
        - n
        - trange
        - user
        """
        with datm.DATMSession(self._config) as datmconfig:
            
            time_utc = time.mktime(datetime.utcnow().timetuple())
            time_utc_old = time_utc - trange*24*60*60
            
            alist = datm.Artist.top(datmconfig, limit=n, after=time_utc_old)
            
            ret = [self.getArtistSE(Artist(mbid=a.mbid, name=a.name), user)
                                                    for a in alist if a.mbid]

            return ret
    
    @rethrow
    def getLFMTop(self, n, user):
        """
        Returns a list of the n top last.fm artists by decreasing value. User 
        returns relevant prices for each artist, otherwise buy price for 
        anonymous users

        Parameters:
        - n
        - trange
        - user
        """
        with datm.DATMSession(self._config) as datmconfig:
            alist = datm.Artist.popular(datmconfig, limit=n)
            
            ret = [self.getArtistSE(Artist(mbid=a.mbid, name=a.name), user)
                                                    for a in alist if a.mbid]
            
            return ret
    
    @rethrow
    def getRecommendedArtists(self, n, user):
        """
        Returns the n top recommended artists for a user
        
        Parameters:
        - n
        - user
        """
        with datm.DATMSession(self._config) as datmconfig:
            
            u = datm.User(datmconfig, name=user.name)
            alist = u.top_artists(limit=n)
            
            ret = [self.getArtistSE(Artist(mbid=a.mbid, name=a.name),
                                                user) for a in alist if a.mbid]
            
            return ret
    
    @rethrow
    def getTradedArtists(self, n, user):
        """
        Returns a list of the n most traded artists by decreasing value. User 
        returns relevant prices for each artist, otherwise buy price for 
        anonymous users.

        Parameters:
        - n
        - user
        """
        with datm.DATMSession(self._config) as datmconfig:
            alist = datm.Artist.most_traded(datmconfig, limit=n)
            
            ret = [self.getArtistSE(Artist(mbid=a.mbid, name=a.name), user)
                                                    for a in alist if a.mbid]

            return ret
    
    @rethrow 
    def getRecentTrades(self, n, user):
        """
        Returns a list of the n most recent trades. User returns relevant 
        prices for each artist, otherwise buy price for anonymous users.

        Parameters:
        - n
        - user
        """
        with datm.DATMSession(self._config) as datmconfig:
            tlist = datm.Trade.recent(datmconfig, limit=n)
            
            ret = [self.getArtistSE(Artist(mbid=t.artist.mbid, 
                                    name=t.artist.name), user) for t in tlist]
            
            return ret
    
    @rethrow
    def getUserData(self, user):
        """
        Returns extended user data for the current user.
        
        Parameters:
        - user
        """
        with datm.DATMSession(self._config) as datmconfig:
            u = datm.User(datmconfig, user)
            
            if not u.persisted:
                print 'Trying a get data on non-existent user ' + user
                raise DataError('User doesn`t exist in database')
            
            basicu = User(name=u.name, points=u.points, profileimage=u.images)
            
            ret = UserData(user=basicu)
            ret.trades = []
            ret.stocks = []
            ret.trophies = []
            ret.league = League(uid=u.league.uid, name=u.league.name,
                                description=u.league.description,
                                icon=u.league.icon)
            
            for t in u.trophies():
                tr = Trophy(uid=u.league.uid, name=t.name, 
                            description=t.description, icon=t.icon)
                
                ret.trophies.append(tr)
            
            for t in u.trades():
                a = self.getArtist(Artist(mbid=t.artist.mbid))
                
                ret.trades.append(Trade(artist=a, price=t.price, time=t.date))
            
            for s in u.stocks:
                a = Artist(mbid=s.mbid, name=s.name, imgurls=s.images)
                
                #the assumption is that if the stock is listed, then it exists 
                #in the DB and no databaseobjectexception would be thrown
                #also, no writes will be done and so no threading errors
                ret.stocks.append(self.getArtistSE(a, basicu))
            
            return ret
        
    def getUserMoney(self, user):
        """
        Returns the current user with money. Requires AuthUser to auth
        
        Parameters:
        - user
        """
        with datm.DATMSession(self._config) as datmconfig:
            u = datm.User(datmconfig, user.user.name)
            
            if not u.persisted:
                print 'Trying to get money on a non-existent user ' + user.user.name
                raise DataError('User doesn`t exist in database')
            
            try:
                u.authenticate(user.session_key)
            except datm.InvalidAuthorisationException:
                raise AuthenticationError('User not authenticated')
            
            return AuthUser(user=User(name=user.user.name, points=u.points,
                        profileimage=u.images),session_key=user.session_key, 
                                                                money=u.money)
    
    def getLeagues(self):
        """
        Returns a list of all the leagues that exist in the game */
        """
        
        with datm.DATMSession(self._config) as datmconfig:
            
            llist = datm.League.all(datmconfig)
            
            ret = []
            
            for l in llist:
                league = League(uid=l.uid, name=l.name, 
                                description=l.description, icon=l.icon)
                
                ret.append(league)
            
            return ret
    
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
        with datm.DATMSession(self._config) as datmconfig:
            
            if league == '':
                l = None
            else:
                l = datm.League(datmconfig, uid=league.uid)
            
            if trange == 1:
                period = 'daily'
            elif trange <= 7:
                period = 'weekly'
            elif trange <= 31:
                period = 'monthly'
            else:
                period = None
                
            ulist = datm.User.top(datmconfig, limit=n, period=period,
                                                                    league=l)
            
            ret = UserLeaderboard(users=[], positions=[])
            
            for u in ulist:
                o = User(name=u.name, profileimage=u.images)
                
                if period == 'daily':
                    o.points = u.daily_points
                elif period == 'weekly':
                    o.points = u.weekly_points
                elif period == 'monthly':
                    o.points = u.monthly_points
                else:
                    o.points = u.points
                
                ret.users.append(o)
                ret.positions.append(u.position(period))
            
            return ret

    def getNearUsers(self, user, trange):
        """
        Returns a list of 10 users with 4 above and 5 below in the leaderboard
        compared to the user provided, including the user's position.  Trange 
        is the number of days the leaderboard is over, rounded to nearest d/w/m

        Parameters:
        - user
        - trange
        """
        with datm.DATMSession(self._config) as datmconfig:
            
            if trange == 1:
                period = 'daily'
            elif trange <= 7:
                period = 'weekly'
            elif trange <= 31:
                period = 'monthly'
            else:
                period = None
            
            u = datm.User(datmconfig, name=user)
            ulist = u.near(up=4, down=5, period=period)
            
            ret = UserLeaderboard(users=[],positions=[u.position(period)])
            for u in ulist:
                ret.users.append(User(name=u.name, points=u.points,
                                                        profileimage=u.images))
            
            return ret
   
    def getGuarantee(self, artist, user):
        """
        Returns the guarantee token (elephant) to the front end
        
        Parameters:
        - artist
        - user
        """
        with datm.DATMSession(self._config) as datmconfig:
            if artist.mbid:
                a = datm.Artist(datmconfig, mbid=artist.mbid)
            elif artist.name:
                a = datm.Artist(datmconfig, name=artist.name)
            else:
                raise DataError('Incorrect artist data')
            
            u = datm.User(datmconfig, user.user.name)
            
            try:
                u.authenticate(user.session_key)
            except datm.InvalidAuthorisationException:
                raise AuthenticationError('User not authenticated')
            
            ma = mechanics.Artist(a)
            price = a.price(owned=u.owns(a))
           
            # Calculating the elephant
            m = hmac.new(datm.Auth(datmconfig).secret.encode('ascii'))
            m.update(u.name)
            m.update(a.mbid)
            m.update(str(int(datetime.utcnow().strftime('%s')) +
                self._time_offset))
            m.update(str(price))
            el = m.hexdigest()
            
            return Guarantee(elephant=el, artist=Artist(mbid=a.mbid, 
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
        with datm.DATMSession(self._config) as datmconfig:
            
            # Calculating the elephant
            m = hmac.new(datm.Auth(datmconfig).secret.encode('ascii'))
            m.update(user.user.name)
            m.update(guarantee.artist.mbid)
            m.update(str(guarantee.time))
            m.update(str(guarantee.price))
            el = m.hexdigest()
            
            #authenticate the elephant
            if guarantee.elephant != el:
                raise DataError('Incorrect elephant')
            
            #check for 15s time (with some leeway)
            if (time_utc - guarantee.time) > 2:
                raise TransientError('Too late')
            
            u = datm.User(datmconfig, name=user.user.name)
            
            try:
                u.authenticate(user.session_key)
            except datm.InvalidAuthorisationException:
                raise AuthenticationError('User not authenticated')
            
            a = datm.Artist(datmconfig, mbid=guarantee.artist.mbid)
            
            if not u.owns(a):
                try:
                    t = mechanics.User(user=u)
                    t.buy(artist=a, price=guarantee.price)
                    return True
                except:
                    return False
            else:
                raise TransientError('User already owns artist')
        

    def sell(self, guarantee, user):
        """
        Sells artist for user, and returns a bool as to whether it was
        successful or not

        Parameters:
        - guarantee
        - user
        """
        with datm.DATMSession(self._config) as datmconfig:
            
            # Calculating the elephant
            m = hmac.new(datm.Auth(datmconfig).secret.encode('ascii'))
            m.update(user.user.name)
            m.update(guarantee.artist.mbid)
            m.update(str(guarantee.time))
            m.update(str(guarantee.price))
            el = m.hexdigest()
            
            #authenticate the elephant
            if guarantee.elephant != el:
                raise DataError('Incorrect elephant')
            
            #check for 15s time (with some leeway)
            if (time_utc - guarantee.time) > 2:
                raise TransientError('Too late')
            
            u = datm.User(datmconfig, name=user.user.name)
            
            try:
                u.authenticate(user.session_key)
            except datm.InvalidAuthorisationException:
                raise AuthenticationError('User not authenticated')
            
            a = datm.Artist(datmconfig, mbid=guarantee.artist.mbid)
            
            if u.owns(a):
                try:
                    t = mechanics.User(user=u)
                    t.sell(artist=a, price=guarantee.price)
                    return True
                except:
                    return False
            else:
                raise TransientError('User doesn\'t own artist')

    def reset(self, user):
        """
        Resets the user to the default state.
        
        Parameters:
        -user
        """
        with datm.DATMSession(self._config) as datmconfig:
            
            u = datm.User(datmconfig, name=user.user.name)
            
            try:
                u.authenticate(user.session_key)
            except:
                raise AuthenticationError('User not authenticated')
           
            try:
                mu = mechanics.User(u)
                mu.reset()
                return True
            except:
                return False
            
            
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
