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

import datm
import config

from datetime import datetime
import time, hmac

lastfm_config = {
    'api_key': config.lastfmcred['api_key'],
    'secret' : config.lastfmcred['secret']
}

db_args = {
    'url': 'sqlite:///:memory:'
}

class SEHandler(object):
    #_config = datm.DATMConfig(lastfm=lastfm_config, db_args=db_args)
    
    def apikey(self):
        """
        Returns the SE API key for sending to last.fm
        """
        return config.lastfmcred['api_key']

    def login(self, username, token):
        """
        If successful, returns the AuthUser with the user session token
        
        Parameters:
        - username
        - token
        """
        with datm.DATMSession(_config):
            try:
                user = datm.user(_config, username)
                sessiontoken = user.getSession(_config, token)
        
                return stoken
            except InvalidAuthorisationException:
                raise LoginException(LoginCode.AUTH, 'User not authenticated')

    def getArtist(self, artist):
        """
        Returns basic artist info. If either the artist or the mbid is unknown,
        then the empty string should be sent.
        
        Parameters:
        - artist
        """
        with datm.DATMSession(_config):
            if not artist.mbid:
                a = datm.artist(_config, mbid = artist.mbid)
            else if not artist.name:
                a = datm.artist(_config, name = artist.name)
            else:
                raise SearchException(SearchCode.ARG, 'Incorrect artist data')
                
            ret = Artist(mbid = a.mbid, name = a.name, imgurls = a.images)
        
            return ret

    def getLightArtist(self, artist):
        """
        Returns only MBID and name. If either artist or mbid are unknown, 
        then the empty string should be sent
        
        Parameters:
        - artist
        """
        with datm.DATMSession(_config):
            if not artist.mbid:
                a = datm.artist(_config, mbid = artist.mbid)
            else if not artist.name:
                a = datm.artist(_config, name = artist.name)
            else:
                raise SearchException(SearchCode.ARG, 'Incorrect artist data')
            
            ret = Artist(mbid = a.mbid, name = a.name)
        
            return ret

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
        with datm.DATMSession(_config):
            if not artist.mbid:
                a = datm.artist(_config, mbid = artist.mbid, user = user)
            else if not artist.name:
                a = datm.artist(_config, name = artist.name, user = user)
            else:
                raise SearchException(SearchCode.ARG, 'Incorrect artist data')
            
            u = datm.user(_config, user.name)
            
            r = Artist(mbid = a.mbid, name = a.name, imgurls = a.images)
            ret = ArtistSE(artist = r, numremaining = a.no_remaining, ownedby 
                                                                    = u.owns(a))
            
            if (u.owns(a)):
                ret.price = a.local_price * 0.97
            else:
                ret.price = a.local_price
            
            return ret

    def getArtistLFM(self, artist):
        """
        Returns the artist info from last.fm for the artist. If either artist
        or mbid are unknown, then the empty string should be sent.
        
        Parameters:
        - artist
        """
        with datm.DATMSession(_config):
            if not artist.mbid:
                a = datm.artist(_config, mbid = artist.mbid)
            else if not artist.name:
                a = datm.artist(_config, name = artist.name)
            else:
                raise SearchException(SearchCode.ARG, 'Incorrect artist data')

            b = ArtistBio(summary = a.summary, content = a.content)       
            
            r = Artist(mbid = a.mbid, name = a.name, imgurls = a.images)
            ret = ArtistLFM(artist = r, streamable = a.streamable, listeners = 
                            a.listeners, plays = a.plays, tags = a.tags, 
similar                             = a.similar, bio = b)
            
            return ret

    def getArtistHistory(self, artist, n):
        """
        Returns a list of tuples of the price of the artist the past n days.
        For new artists the empty list is returned.
        
        Parameters:
        - artist
        - n
        """
        with datm.DATMSession(_config):
            if not artist.mbid:
                a = datm.artist(_config, mbid = artist.mbid)
            else if not artist.name:
                a = datm.artist(_config, name = artist.name)
            else:
                raise SearchException(SearchCode.ARG, 'Incorrect artist data')
            
            time_now = datetime.now()
            time_utc = time.mktime(time_now.timetuple()) - time.timezone
            time_utc_old = time_utc - n*24*60*60
            
            ret = ArtistHistory()
            ret.histvalue = a.history(_config, after = time_utc_old)
            
            return ret

    def searchArtist(self, text):
        """
        returns a list of possible artists from a partial string. Ordered by
        decreasing relevance. List size is limited to 5 elements.
        
        Parameters:
        - text
        """
        with datm.DATMSession(_config):
            alist = datm.artist.search(_config, text, limit = 5)
            
            ret = [Artist(mbid = a.mbid, name = a.name, imgurls = a.images) for
                                                                    a in alist]
            
            return ret

    def getSETop(self, n):
        """
        Returns a list of the n top SE artists by decreasing value.

        Parameters:
        - n
        """
        with datm.DATMSession(_config):
            alist = datm.artist.top(_config, limit = n)
            
            ret = [Artist(mbid = a.mbid, name = a.name, imgurls = a.images) for
                                                                    a in alist]

            return ret
    
    def getLFMTop(self, n):
        """
        Returns a list of the n top last.fm artists by decreasing value.

        Parameters:
        - n
        """
        with datm.DATMSession(_config):
            alist = datm.artist.popular(_config, limit = n)
            
            ret = [Artist(mbid = a.mbid, name = a.name, imgurls = a.images) for
                                                                    a in alist]
            
            return ret

    def getTradedArtists(self, n):
        """
        Returns a list of the n most traded artists by decreasing value.

        Parameters:
        - n
        """
        with datm.DATMSession(_config):
            alist = datm.artist.most_traded(_config, limit = n)
            
            ret = [Artist(mbid = a.mbid, name = a.name, imgurls = a.images) for
                                                                    a in alist]

            return ret
    
    def getRecentTrades(self, n):
        """
        Returns a list of the n most recent trades

        Parameters:
        - n
        """
        with datm.DATMSession(_config):
            tlist = datm.trade.recent(_config, limit = n)
            
            ret = [Artist(mbid = t.mbid, name = t.name, imgurls = t.images) for
                                                                    t in tlist]
            
            return ret

    def getUserData(self, user):
        """
        Returns extended user data for the current user.
        
        Parameters:
        - user
        """
        with datm.DATMSession(_config):
            u = datm.user(_config, user.name)
            
            basicu = User(name = u.name, points = u.points)
            
            ret = UserData(user = basicu)
            ret.trades = []
            ret.stocks = []
            ret.trophies = [Trophy(name = u.trophies.name, description = 
                                                        u.trophies.description)]
            ret.league = League(name = u.league.name, description = 
                                    u.league.description, icon = u.league.icon)
           
            for t in u.trades:
                a = Artist(mbid = t.Artist.mbid, name = t.Artist.name, imgurls 
                                                            = t.Artist.images)
                
                ret.trades.append(Trade(artist = a, price = t.price, time = 
                                                                        t.time))
            
            for t in u.stocks:
                a = Artist(mbid = t.Artist.mbid, name = t.Artist.name, imgurls 
                                                            = t.Artist.images)
                
                ret.stocks.append(ArtistSE(artist = a, price = t.price, 
                                                numremaining = no_remaining)
            
            return ret
        
    def getUserMoney(self, user):
        """
        Returns the current user with money. Requires AuthUser to auth
        
        Parameters:
        - user
        """
        with datm.DATMSession(_config):
            u = datm.user(_config, user.name, user.session_key)
            
            return AuthUser(name = user.name, session_key = user.session_key, 
                                                                money = u.money)

    
    def getTopUsers(self, n, league):
        """
        Returns the n top users by decreasing value in the given league.

        Parameters:
        - n
        - league
        """
        with datm.DATMSession(_config):
            ulist = datm.user.top(_config, limit = n, league = league.name)
            
            return UserLeaderboard(users = [User(name = u.name) for u in ulist])

    def getNearUsers(self, user):
        """
        Returns a list of 10 users with 4 above and 5 below in the leaderboard
        compared to the user provided, including the user's position.

        Parameters:
        - user
        """
        with datm.DATMSession(_config):
            ulist = datm.user.near(_config, name = user.name)
            
            return UserLeaderboard(users = [User(name = u.name) for u in ulist])
   
    def getGuarantee(self, artist, user):
        """
        Returns the guarantee token (elephant) to the front end
        
        Parameters:
        - artist
        - user
        """
        with datm.DATMSession(_config):
            if not artist.mbid:
                a = datm.artist(_config, mbid = artist.mbid, user = user)
            else if not artist.name:
                a = datm.artist(_config, name = artist.name, user = user)
            else:
                raise TransactionException(TransactionCode.ARG, 'Incorrect \
                                                                artist data')
            
            u = datm.user(_config, user.name)
            
            if (u.owns(a)):
                price = a.local_price * 0.97
            else:
                price = a.local_price
           
            # Calculating the elephant
            time_now = datetime.now()
            time_utc = time.mktime(time_now.timetuple()) - time.timezone

            m = hmac.new(datm.auth.secret(_config))
            m.update(str(time_utc))
            m.update(str(price))
            el = m.hexdigest()
            
            return Guarantee(elephant = el, artist = Artist(mbid = a.mbid, 
                            name = a.name, imgurls = a.images), price = price,   
                            time = time_utc)
        

    def buy(self, guarantee, user):
        """
        Buys artist for user, and returns a bool as to whether it was
        successful or not

        Parameters:
        - guarantee
        - user
        """
        with datm.DATMSession(_config):
            
            # Calculating the elephant
            time_now = datetime.now()
            time_utc = time.mktime(time_now.timetuple()) - time.timezone

            m = hmac.new(datm.auth.secret(_config))
            m.update(str(time_utc))
            m.update(str(guarantee.price))
            el = m.hexdigest() 
            
            #authenticate the elephant
            if guarantee.elephant != el:
                raise TransactionException(code = TransactionCode.ARG, message  
                                                        = 'Incorrect Elephant')
            
            #check for 15s time (with some leeway)
            if (time_utc - guarantee.time) > 17:
                raise TransactionException(code = TransactionCode.TIME, message 
                                                                  = 'Too late')
            
            u = datm.user(_config, user = user.name)
            a = datm.artist(_config, mbid = guarantee.artist.mbid)
            
            try:
                t = datm.trade.buy(_config, user = u, artist = a, price = 
                                                                guarantee.price)
            except NoStockRemainingException:
                raise TransactionException(code = TransactionCode.NUM, message 
                                                         = 'No stock remaining')

        

    def sell(self, guarantee, user):
        """
        Sells artist for user, and returns a bool as to whether it was
        successful or not

        Parameters:
        - guarantee
        - user
        """
        with datm.DATMSession(_config):
            
            # Calculating the elephant
            time_now = datetime.now()
            time_utc = time.mktime(time_now.timetuple()) - time.timezone

            m = hmac.new(datm.auth.secret(_config))
            m.update(str(time_utc))
            m.update(str(guarantee.price))
            el = m.hexdigest() 
            
            #authenticate the elephant
            if guarantee.elephant != el:
                raise TransactionException(code = TransactionCode.ARG, message  
                                                        = 'Incorrect Elephant')
            
            #check for 15s time (with some leeway)
            if (time_utc - guarantee.time) > 17:
                raise TransactionException(code = TransactionCode.TIME, message 
                                                                  = 'Too late')
            
            u = datm.user(_config, user = user.name)
            a = datm.artist(_config, mbid = guarantee.artist.mbid)
            
            try:
                t = datm.trade.sell(_config, user = u, artist = a, price = 
                                                                guarantee.price)
            except UserIsLyingToYouException:
                raise TransactionException(code = TransactionCode.NONE, message 
                                                          = 'User cannot sell')
        



processor = ScrobbleExchange.Processor(SEHandler())
transport = TSocket.TServerSocket(port=9090)
tfactory = TTransport.TBufferedTransportFactory()
pfactory = TBinaryProtocol.TBinaryProtocolFactory()

server = TServer.TThreadPoolServer(processor, transport, tfactory, pfactory)

print 'Starting the server...'
server.serve()
print 'done.'
