# Python Server

from se_api import ScrobbleExchange
from se_api.ttypes import *
from se_api.constants import *

from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
from thrift.server import TServer

from datetime import datetime
import time, hmac

class SEHandler(object):
   
    def apikey(self):
        """
        Returns the SE API key for sending to last.fm
        """
        return '9dd5403b2dccbc443222d331d66b4424'

    def login(self, token):
        """
        If successful, returns the AuthUser with the user session token
        
        Parameters:
        - username
        - token
        """
       
        ret = AuthUser(User(name = 'fiwl',profileimage='http://userserve-ak.'\
            'last.fm/serve/126/8270359.jpg'), session_key = 'randomstringhere', 
            money = 9399)
        return ret

    def getArtist(self, artist):
        """
        Returns basic artist info. If either the artist or the mbid is unknown,
        then the empty string should be sent.
        
        Parameters:
        - artist
        """
        
        artists = {
            'Coldplay':Artist(mbid = '', name = 'Coldplay', imgurls = {
                'mega': 'http:\/\/userserve-' \
                 'ak.last.fm\/serve\/500\/75646980\/Coldplay+PNG.png',
                'extralarge':'http:\/\/userserve-' \
                 'ak.last.fm\/serve\/252\/75646980.png',
                'large': 'http://userserve-ak.last.fm/serve/126/75646980.png',
                'medium': 'http://userserve-ak.last.fm/serve/64/75646980.png',
                'small': 'http://userserve-ak.last.fm/serve/34/75646980.png'
                }
            ),
            'Daft Punk':Artist(mbid = '', name = 'Daft Punk', imgurls = {
                'mega': 'http:\/\/userserve-' \
                'ak.last.fm\/serve\/500\/4183432\/Daft+Punk+daftpunk_1.jpg',
                'extralarge': 'http:\/\/userserve-' \
                'ak.last.fm\/serve\/252\/4183432.jpg',
                'large': 'http://userserve-ak.last.fm/serve/126/4183432.jpg',
                'medium': 'http://userserve-ak.last.fm/serve/64/4183432.jpg',
                'small': 'http://userserve-ak.last.fm/serve/34/4183432.jpg'
                }
            ),
            'Gorillaz':Artist(mbid = '', name = 'Gorillaz', imgurls = {
                'mega': 'http:\/\/userserve-' \
                'ak.last.fm\/serve\/_\/411274\/Gorillaz.jpg',
                'extralarge': 'http:\/\/userserve-' \
                'ak.last.fm\/serve\/252\/411274.jpg'}
            ),
            'Flight of the Conchords':Artist(mbid = '', name = 
                                                    'Flight of the Conchords', 
            imgurls = {
                'mega': 'http://userserve-ak.last.fm' \
                '/serve/_/22957595/Flight+of+the+Conchords+flight.jpg',
                'extralarge': 'http://userserve-' \
                'ak.last.fm/serve/252/22957595.jpg',
                'large': 'http://userserve-ak.last.fm/serve/126/22957595.jpg',
                'medium': 'http://userserve-ak.last.fm/serve/64/22957595.jpg',
                'small': 'http://userserve-ak.last.fm/serve/34/22957595.jpg'
                }
            ),
            'The Killers':Artist(mbid = '', name = 'The Killers', imgurls = {
                'mega': 'http://userserve-' \
                'ak.last.fm/serve/500/82785611/The+Killers+tumblr_1280.png',
                'extralarge': 'http://userserve-' \
                'ak.last.fm/serve/252/82785611.png',
                'large': 'http://userserve-ak.last.fm/serve/126/82785611.png',
                'medium': 'http://userserve-ak.last.fm/serve/64/82785611.png',
                'small': 'http://userserve-ak.last.fm/serve/34/82785611.png'
                }
            ),
            'Hans Zimmer':Artist(mbid = '', name = 'Hans Zimmer', imgurls = {
                'mega': 'http://userserve-' \
                'ak.last.fm/serve/500/73701504/Hans+Zimmer+hz4.png',
                'extralarge': 'http://userserve-' \
                'ak.last.fm/serve/252/73701504.png',
                'large': 'http://userserve-ak.last.fm/serve/126/73701504.png',
                'medium': 'http://userserve-ak.last.fm/serve/64/73701504.png',
                'small': 'http://userserve-ak.last.fm/serve/34/73701504.png'
                }
            ),
            'A random band with a missing image and a long name! (and '\
            'punctuation)':Artist(mbid = '', name = 'A random band with a '\
            'missing image and a long name! (and punctuation)', imgurls = {}
            )
        }
      
        return artists[artist.name]

    def getLightArtist(self, artist):
        pass

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
        artists = {
            'Coldplay':ArtistSE(artist = self.getArtist(artist), price = 2500, 
                numremaining = 10, points = 242, dividend=200, ownedby = True),
            'Daft Punk':ArtistSE(artist = self.getArtist(artist), price = 2200,
                numremaining = 17, points = 420, dividend=100, ownedby = False),
            'Gorillaz':ArtistSE(artist = self.getArtist(artist), price = 2300,
                numremaining = 167, points = 333, dividend=103 ownedby = False),
            'Flight of the Conchords':ArtistSE(artist = self.getArtist(artist), 
                price = 2401, numremaining = 120, points = 309, ownedby = 
                False, dividend=302),
            'The Killers':ArtistSE(artist = self.getArtist(artist), price = 
                1920, numremaining=38, points=523, dividend=12, ownedby = True),
            'Hans Zimmer':ArtistSE(artist = self.getArtist(artist), price = 
                1605, numremaining=289,points=688, dividend=34, ownedby = True),
            'A random band with a missing image and a long name! (and '\
            'punctuation)':ArtistSE(artist = self.getArtist(artist), price = 
                100,numremaining=1829, points=444, dividend=200, ownedby = True)
        }
        
        return artists[artist.name]

    def getArtistLFM(self, artist, user):
        """
        Returns the artist info from last.fm for the artist. If either artist
        or mbid are unknown, then the empty string should be sent.
        
        Parameters:
        - artist
        """
        artists = {
            'Coldplay':ArtistLFM(artist = self.getArtist(artist), streamable = 
                True, listeners = 1000, plays = 1000, tags = ['one','two'], 
                similar = [], bio = ArtistBio(content = '', summary = 
                """Coldplay is a British <a 
                href="http://www.last.fm/tag/alternative%20rock" 
                class="bbcode_tag" rel="tag">alternative rock</a> band, formed 
                in London, United Kingdom in 1997. The band comprises vocalist 
                and pianist <a href="http://www.last.fm/music/Chris+Martin" 
                class="bbcode_artist">Chris Martin</a>, lead guitarist <a 
                href="http://www.last.fm/music/Jonny+Buckland" 
                class="bbcode_artist">Jonny Buckland</a>, bassist <a 
                href="http://www.last.fm/music/Guy+Berryman" 
                class="bbcode_artist">Guy Berryman</a>, and drummer <a 
                href="http://www.last.fm/music/Will+Champion" 
                class="bbcode_artist">Will Champion</a>. Having released four 
                successful albums, (all of which debuted at #1 on the UK album 
                chart) Coldplay have also achieved great success with their 
                singles, such as <a title="Coldplay &ndash; Yellow" 
                href="http://www.last.fm/music/Coldplay/_/Yellow" 
                class="bbcode_track">Yellow</a>, <a title="Coldplay &ndash; 
                Speed of Sound" 
                href="http://www.last.fm/music/Coldplay/_/Speed+of+Sound" 
                class="bbcode_track" >Speed of Sound</a>, the Grammy-winning <a 
                title="Coldplay &ndash; Clocks" 
                href="http://www.last.fm/music/Coldplay/_/Clocks" 
                class="bbcode_track">Clocks</a> and the US and UK #1 single <a 
                title="Coldplay &ndash; Viva la Vida" 
                href="http://www.last.fm/music/Coldplay/_/Viva+la+Vida" 
                class="bbcode_track">Viva la Vida</a>. Frontman Chris Martin 
                credits 1980s Norwegian pop band <a 
                href="http://www.last.fm/music/a-ha" 
                class="bbcode_artist">a-ha</a> for inspiring him to form his 
                own band."""
                )),
            'Daft Punk':ArtistLFM(
                artist = self.getArtist(artist),
                streamable = True, listeners = 1500, plays = 900,
                tags = ['one','three'], 
                similar = [self.getArtist(Artist(mbid = '', name = 'Daft '\
                    'Punk')), self.getArtist(Artist(mbid ='',name = 'A random'\
                    ' band with a missing image and a long name! (and'\
                    ' punctuation)'))],
                bio = ArtistBio(summary = '', content = '')),
            'Gorillaz':ArtistLFM(
                artist = self.getArtist(artist),
                streamable = True, listeners = 700, plays = 1300,
                tags = ['one','two'], 
                similar = [self.getArtist(Artist(mbid = '', name = 'Daft '\
                    'Punk')), self.getArtist(Artist(mbid ='',name = 'A random'\
                    ' band with a missing image and a long name! (and'\
                    ' punctuation)'))],
                bio = ArtistBio(summary = '', content = '')),
            'Flight of the Conchords':ArtistLFM(
                artist = self.getArtist(artist),
                streamable = True, listeners = 700, plays = 1300, 
                tags = ['one','two'],
                similar = [self.getArtist(Artist(mbid = '', name = 'Daft '\
                    'Punk')), self.getArtist(Artist(mbid ='',name = 'A random'\
                    ' band with a missing image and a long name! (and'\
                    ' punctuation)'))],
                bio = ArtistBio(summary = '', content = '')),
            'The Killers':ArtistLFM(
                artist = self.getArtist(artist),
                streamable = True, listeners = 700, plays = 1300,
                tags = ['one','two'], 
                similar = [self.getArtist(Artist(mbid = '', name = 'Daft '\
                    'Punk')), self.getArtist(Artist(mbid ='',name = 'A random'\
                    ' band with a missing image and a long name! (and'\
                    ' punctuation)'))],
                bio = ArtistBio(summary = '', content = '')),
            'Hans Zimmer':ArtistLFM(
                artist = self.getArtist(artist),
                streamable = True, listeners = 700, plays = 1300,
                tags = ['one','two'], 
                similar = [self.getArtist(Artist(mbid = '', name = 'Daft '\
                    'Punk')), self.getArtist(Artist(mbid ='',name = 'A random'\
                    ' band with a missing image and a long name! (and'\
                    ' punctuation)'))],
                bio = ArtistBio(summary = '', content = '')),
            'A random band with a missing image and a long name! (and '\
            'punctuation)':ArtistLFM(
                artist = self.getArtist(artist), 
                streamable = True, listeners = 10, plays = 200,
                tags = ['one','two'],
                similar = [self.getArtist(Artist(mbid = '', name = 'Daft '\
                    'Punk')), self.getArtist(Artist(mbid ='',name = 'A random'\
                    ' band with a missing image and a long name! (and'\
                    ' punctuation)'))],
                bio = ArtistBio(summary = '', content = ''))
        }
        
        return artists[artist.name]

    def getArtistHistory(self, artist, n):
        pass
        

    def searchArtist(self, text, n, page):
        
        artists = ['Daft Punk', 'Gorillaz', 'Flight of the Conchords', 'The '\
'Killers', 'Hans Zimmer', 'A random band with a missing image and a long name!'\
' (and punctuation)']

        results = [a for a in artists if text in a]
        ret = [self.getArtist(Artist(mbid = '', name = a)) for a in results if 
                                                                results != []]
       
        return ret

    def getSETop(self, n, trange):
        """
        Returns a list of the n top SE artists by decreasing value.

        Parameters:
        - n
        """
        top = [self.getArtist(Artist(mbid = '', name = 'Coldplay')), 
                self.getArtist(Artist(mbid = '',
                                    name = 'Flight of the Conchords')),
                self.getArtist(Artist(mbid = '', name = 'Daft Punk')), 
                self.getArtist(Artist(mbid = '', name = 'The Killers')), 
                self.getArtist(Artist(mbid = '', name = 'Hans Zimmer'))]
        
        return top
    
    def getLFMTop(self, n, trange):
        pass

    def getTradedArtists(self, n):
        pass
    
    def getRecentTrades(self, n):
        pass

    def getUserData(self, user):
        """
        Returns extended user data for the current user.
        
        Parameters:
        - user
        """
        u = User(name = user)
        ret = UserData(user = User(name = user, points = 242), trades = [], 
            stocks = [self.getArtistSE(Artist(name = 'Coldplay'),u), 
            self.getArtistSE(Artist(name ='The Killers'),u), 
            self.getArtistSE(Artist(name = 'Hans Zimmer'),u),
            self.getArtistSE(Artist(name = 'A random band with a missing '\
                'image and a long name! (and punctuation)'),u)],             
            trophies = [], league = League(name = 'bronze'))
        
        return ret
        
    def getUserMoney(self, user):
        """
        Returns the current user with money. Requires AuthUser to auth
        
        Parameters:
        - user
        """
        
        ret = user
        ret.money = 2903
        ret.name.profileimage = 'http://userserve-ak.last.fm/'\
                                'serve/126/8270359.jpg'
        
        return ret
    
    def getTopUsers(self, n, league, trange):
        
        us = {
            'neil-s':User(name = 'neil-s', points = 70),
            'joebateson':User(name = 'joebateson', points = 40),
            'rand':User(name = 'rand', points = 20)
        }
        
        top = ['neil-s','joebateson','rand']
        
        ret = UserLeaderboard(users=[us[t] for t in top])
        
        return ret

    def getNearUsers(self, user):
        pass
   
    def getGuarantee(self, artist, user):
        """
        Returns the guarantee token (elephant) to the front end
        
        Parameters:
        - artist
        - user
        """
        return Guarantee(elephant = 'elephant', artist =self.getArtist(artist), 
                price = 393, time = 1361816537)

    def buy(self, guarantee, user):
        """
        Buys artist for user, and returns a bool as to whether it was
        successful or not

        Parameters:
        - guarantee
        - user
        """
        return True

    def sell(self, guarantee, user):
        """
        Sells artist for user, and returns a bool as to whether it was
        successful or not

        Parameters:
        - guarantee
        - user
        """
        return True
       
processor = ScrobbleExchange.Processor(SEHandler())
transport = TSocket.TServerSocket(port=9090)
tfactory = TTransport.TBufferedTransportFactory()
pfactory = TBinaryProtocol.TBinaryProtocolFactory()

server = TServer.TThreadPoolServer(processor, transport, tfactory, pfactory)

print 'Starting the server...'
server.serve()
print 'done.'
