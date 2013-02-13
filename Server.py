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

#import datm
#import config

#lastfm_config = {
    #'api_key': config.lastfmcred['api_key'],
    #'secret' : config.lastfmcred['secret']
#}

#db_args = {
    #'url': 'sqlite:///:memory:'
#}

class SEHandler(object):
    #_config = datm.DATMConfig(lastfm=lastfm_config, db_args=db_args)
    
    def apikey(self):
        """
        Returns the SE API key for sending to last.fm
        """
        #return config.lastfmcred['apikey']
        pass

    def login(self, username, token):
        """
        If successful, returns the user session token.

        Parameters:
        - username
        - token
        """
        #with datm.DATMSession(_config):
            #try:
                #user = datm.User(self._config, username)
                #stoken = user.getSession(self._config, token)
        
                #return stoken
            #except InvalidAuthorisationException:
                #l = LoginException()
                #l.code = LoginCode.AUTH
                #l.message = 'User not authenticated'
                #raise l
        pass

    def getArtist(self, artist, user, token):
        """
        Returns basic artist info. If either the artist or the mbid is unknown,
        then the empty string should be sent. User will add the `ownedby'
        property to artist

        Parameters:
        - artist
        - user
        - token
        """
        #with datm.DATMSession(_config):
            #if not artist.mbid:
                #a = datm.Artist(self._config, mbid = artist.mbid, user=user)
            #else if not artist.name:
                #a = datm.Artist(self._config, name = artist.name, user = user)
            #else:
                #s = SearchException()
                #s.code = SearchCode.ARG
                #s.message = 'Incorrect artist data'
                #raise s
                
            #u = datm.User(self._config, user.name, token)
            
            #ret = Artist()
            #ret.mbid = a.mbid
            #ret.name = a.name
            #ret.imgurls = a.images
            #ret.ownedby = u.owns(a)
        
            #return ret
        pass

    def getLightArtist(self, artist, user):
        """
        Returns only MBID and name. If either artist or mbid are unknown, then
        the empty string should be sent

        Parameters:
        - artist
        - user
        """
        #with datm.DATMSession(_config):
            #if not artist.mbid:
                #a = datm.Artist(self._config, mbid = artist.mbid, user=user)
            #else if not artist.name:
                #a = datm.Artist(self._config, name = artist.name, user = user)
            #else:
                #s = SearchException()
                #s.code = SearchCode.ARG
                #s.message = 'Incorrect artist data'
                #raise s
            
            #ret = Artist()
            #ret.mbid = a.mbid
            #ret.name = a.name
        
            #return ret
        pass

    def getArtistHistory(self, artist):
        """
        Returns a list of tuples of the price of the artist over time. For new
        artists the empty list is returned.

        Parameters:
        - artist
        """
        pass

    def getArtistSE(self, artist, user, token):
        """
        Returns the data from our db. If the artist isn't there, the data gets
        on-demand pulled. If either artist or mbid are unknown, then the empty
        string should be sent. User will add the `ownedby' property to artist

        Parameters:
        - artist
        - user
        - token
        """
        #with datm.DATMSession(_config):
            #if not artist.mbid:
                #a = datm.Artist(self._config, mbid = artist.mbid, 
                    #user=user)
            #else if not artist.name:
                #a = datm.Artist(self._config, name = artist.name, user = 
                    #user)
            #else:
                #s = SearchException()
                #s.code = SearchCode.ARG
                #s.message = 'Incorrect artist data'
                #raise s
            
            #u = datm.User(self._config, user.name, token)
            
            #r = Artist()
            #r.mbid = a.mbid
            #r.name = a.name
            #r.imgurls = a.images
            #r.ownedby = u.owns(a)
            
            #ret = ArtistSE()
            #ret.artist = r
            #ret.price = a.price
            #ret.num_remaining = a.no_remaining
            
            #return ret
        pass

    def getArtistLFM(self, artist, user, token):
        """
        Returns the artist info from last.fm for the artist. If either artist
        or mbid are unknown, then the empty string should be sent. User will add
        the `ownedby' property to the artist

        Parameters:
        - artist
        - user
        - token
        """
        #with datm.DATMSession(_config):
            #if not artist.mbid:
                #a = datm.Artist(self._config, mbid = artist.mbid, 
                    #user=user)
            #else if not artist.name:
                #a = datm.Artist(self._config, name = artist.name, user = 
                    #user)
            #else:
                #s = SearchException()
                #s.code = SearchCode.ARG
                #s.message = 'Incorrect artist data'
                #raise s
            
            #u = datm.User(self._config, user.name, token)
            
            #r = Artist()
            #r.mbid = a.mbid
            #r.name = a.name
            #r.imgurls = a.images
            #r.ownedby = u.owns(a)
            
            #ret = ArtistLFM()
            #ret.artist = a.streamable
            #ret.listeners = a.listeners
            #ret.plays = a.plays
            #ret.similar = a.similar
            #ret.bio = a.bio
            
            #return ret
        
        pass

    def searchArtist(self, text):
        """
        returns a list of possible artists from a partial string. Ordered by
        decreasing relevance. List size is limited to 5 elements.

        Parameters:
        - text
        """
        pass

    def getTopArtists(self, n, tag):
        """
        Returns a list of the n top artists by decreasing value. By default,
        tag should be the empty string, and only used if you want specific tag
        access.

        Parameters:
        - n
        - tag
        """
        pass

    def getTradedArtists(self, n):
        """
        Returns a list of the n most traded artists by decreasing value.

        Parameters:
        - n
        """
        pass

    def getRecentTrades(self, n):
        """
        Returns a list of the n most recent trades

        Parameters:
        - n
        """
        pass

    def getRecentArtistTrades(self, n):
        """
        Returns a list of the n most recent trades of this artist

        Parameters:
        - n
        """
        pass

    def getUserData(self, user, token):
        """
        Returns extended user data for the current user. Requires the session
        token for validation

        Parameters:
        - user
        - token
        """
        pass

    def getUserInfo(self, userstr):
        """
        Returns extended user data for the user in the string. Mostly, used for
        profile pages

        Parameters:
        - userstr
        """
        pass

    def getTopUsers(self, n, league):
        """
        Returns the n top users by decreasing value in the given league.

        Parameters:
        - n
        - league
        """
        pass

    def getNearUsers(self, user, token):
        """
        Returns a list of 10 users with 4 above and 5 below in the leaderboard
        compared to the user provided, including the user's position. Requires
        the session token for validation

        Parameters:
        - user
        - token
        """
        pass

    def getGuarantee(self, artist):
        """
        Returns the guarantee token (elephant) to the front end

        Parameters:
        - artist
        """
        pass

    def buyArtist(self, transaction, user):
        """
        Buys artist for user, and returns the new value of that stock in the
        game.

        Parameters:
        - transaction
        - user
        """
        pass

    def sellArtist(self, transaction, user):
        """
        Sells artist for user, and returns the new value of that artist.

        Parameters:
        - transaction
        - user
        """
        pass


processor = ScrobbleExchange.Processor(SEHandler())
transport = TSocket.TServerSocket(port=9090)
tfactory = TTransport.TBufferedTransportFactory()
pfactory = TBinaryProtocol.TBinaryProtocolFactory()

server = TServer.TSimpleServer(processor, transport, tfactory, pfactory)

print 'Starting the server...'
server.serve()
print 'done.'
