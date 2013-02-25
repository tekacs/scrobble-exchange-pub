from django.template import RequestContext, loader
from django.http import HttpResponse
from django.shortcuts import render_to_response
import models
from utils import json_response

import random

## Import thrift stuff

# from se_api import ScrobbleExchange
# from se_api import ttypes

# from thrift import Thrift
# from thrift.transport import TSocket
# from thrift.transport import TTransport
# from thrift.protocol import TBinaryProtocol
## End of thrift

#try:
    ## Connect to the API server
    #transport = TSocket.TSocket('localhost', 9090)
    #transport = TTransport.TBufferedTransport(transport)
    #protocol = TBinaryProtocol.TBinaryProtocol(transport)
    #client = ScrobbleExchange.Client(protocol)
    #transport.open()
    ## End

def home(request):
    # Dummy artist data
    user_data = models.UserData()
    user_data.stocks = [
        {
            'artist': {
                'name': 'Coldplay',
                'imgurls': {
                    'mega': 'http:\/\/userserve-ak.last.fm\/serve\/500\/75646980\/Coldplay+PNG.png',
                    'extralarge': 'http:\/\/userserve-ak.last.fm\/serve\/252\/75646980.png'
                    # in real data, get all available image urls
                }
            },
            'price': 2500
        }, 
        {  
            'artist': {
                'name': 'Daft Punk',
                'imgurls': {
                    'mega': 'http:\/\/userserve-ak.last.fm\/serve\/500\/4183432\/Daft+Punk+daftpunk_1.jpg',
                    'extralarge': 'http:\/\/userserve-ak.last.fm\/serve\/252\/4183432.jpg'    
                    # in real data, get all available image urls
                }
            },
            'price': 2200
        },
        {
            'artist': {
                'name': 'Gorillaz',
                'imgurls': {
                    'mega': 'http:\/\/userserve-ak.last.fm\/serve\/_\/411274\/Gorillaz.jpg',
                    'extralarge': 'http:\/\/userserve-ak.last.fm\/serve\/252\/411274.jpg'    
                    # in real data, get all available image urls
                }
            },
            'price': 2300
        },
        {
            'artist': {
                'name': 'A random band with a missing image and a long name! (and punctuation)',
                'imgurls': {   
                    # in real data, get all available image urls
                }
            },
            'price': 100
        }]
    user_data.user = {'money': 140512, 'points': 242}
    user_data.portfolio_worth = sum(artist_SE['price'] for artist_SE in user_data.stocks)
    
    ##Done with the API
    # api_user_data = client.getUserData(request.session['user'])
    # authorized_user = ttypes.AuthUser(name = request.session['user'], 
    #                   session_key = 'thekeyyougot')
    
    # user_data = __portfolio(request.session['user'])
    # user_data.stocks = []
    # for artistse in api_user_data.stocks:
    #   a = {'name': artistse.artist.name, 'imgurls' = artistse.artist.imgurls}
    #   stocks.append({'artist': a, 'price': artistse.price})
    # user_data.user = {'money': client.getUserMoney(authorized_user), 
    #                   'points': user_data.user.points}
    # user_data.worth = sum(artist.price for artist in api_user_data.stocks)
    
    return render_to_response(
        'index.html',
        {'user_data': user_data},
        context_instance=RequestContext(request)
        )

def artists(request):
    # artistlist = se_api.lastfm.chart.get_top_artists()
    artist1 = models.Artist()
    artist1.name = 'Iron Maiden'
    artist2 = models.Artist()
    artist2.name = 'Foo Fighters'
    artistlist = [artist1, artist2]

    top_SE_artists = [
        {
            'artist': {
                'name': 'Coldplay',
                'imgurls': {
                    'mega': 'http:\/\/userserve-ak.last.fm\/serve\/500\/75646980\/Coldplay+PNG.png',
                    'extralarge': 'http:\/\/userserve-ak.last.fm\/serve\/252\/75646980.png',
                    'large': 'http://userserve-ak.last.fm/serve/126/75646980.png',
                    'medium': 'http://userserve-ak.last.fm/serve/64/75646980.png',
                    'small': 'http://userserve-ak.last.fm/serve/34/75646980.png'                    
                }
            },
            'price': 2542,
            'points': 242
        },
        {
            'artist': {
                'name': 'Flight of the Conchords',
                'imgurls': {
                    'mega': 'http://userserve-ak.last.fm/serve/_/22957595/Flight+of+the+Conchords+flight.jpg',
                    'extralarge': 'http://userserve-ak.last.fm/serve/252/22957595.jpg',
                    'large': 'http://userserve-ak.last.fm/serve/126/22957595.jpg',
                    'medium': 'http://userserve-ak.last.fm/serve/64/22957595.jpg',
                    'small': 'http://userserve-ak.last.fm/serve/34/22957595.jpg'
                }
            },
            'price': 2401,
            'points': 309
        },        
        {  
            'artist': {
                'name': 'Daft Punk',
                'imgurls': {
                    'mega': 'http:\/\/userserve-ak.last.fm\/serve\/500\/4183432\/Daft+Punk+daftpunk_1.jpg',
                    'extralarge': 'http:\/\/userserve-ak.last.fm\/serve\/252\/4183432.jpg',
                    'large': 'http://userserve-ak.last.fm/serve/126/4183432.jpg',
                    'medium': 'http://userserve-ak.last.fm/serve/64/4183432.jpg',
                    'small': 'http://userserve-ak.last.fm/serve/34/4183432.jpg'
                }
            },
            'price': 2200,
            'points': 420
        },
        {  
            'artist': {
                'name': 'The Killers',
                'imgurls': {
                    'mega': 'http://userserve-ak.last.fm/serve/500/82785611/The+Killers+tumblr_1280.png',
                    'extralarge': 'http://userserve-ak.last.fm/serve/252/82785611.png',
                    'large': 'http://userserve-ak.last.fm/serve/126/82785611.png',
                    'medium': 'http://userserve-ak.last.fm/serve/64/82785611.png',
                    'small': 'http://userserve-ak.last.fm/serve/34/82785611.png'
                }
            },
            'price': 1920,
            'points': 523
        },
        {  
            'artist': {
                'name': 'Hans Zimmer',
                'imgurls': {
                    'mega': 'http://userserve-ak.last.fm/serve/500/73701504/Hans+Zimmer+hz4.png',
                    'extralarge': 'http://userserve-ak.last.fm/serve/252/73701504.png',
                    'large': 'http://userserve-ak.last.fm/serve/126/73701504.png',
                    'medium': 'http://userserve-ak.last.fm/serve/64/73701504.png',
                    'small': 'http://userserve-ak.last.fm/serve/34/73701504.png'
                }
            },
            'price': 1605,
            'points': 688
        },
    ]

    rising_SE_artists = list(top_SE_artists)
    random.shuffle(rising_SE_artists)

    recommended_artists = list(top_SE_artists)
    random.shuffle(recommended_artists)
    
    ## Done with the API
    # authorized_user = ttypes.AuthUser(name = request.session['user'], 
    #                   session_key = 'thekeyyougot')
    # artist1 = ttypes.Artist(name = 'Iron Maiden')
    # artist2 = ttypes.Artist(name = 'Foo Fighters')
    # artistlist = [artist1, artist2]
   
    # api_top_artists = client.getSETop(5)
    # top_SE_artists = []
    # for i in api_top_artists:
    #   a = client.getArtistSE(i, authorized_user)
    #   artist = {'name': i.name, 'imgurls': i.imgurls}
    #   top_SE_artists.append('artist':artist, 'price': a.price, 'points' = 
    #   a.points)

    return render_to_response('artists.html', {
        'artistlist': artistlist, 
        'top_SE_artists': top_SE_artists, 
        'top_LFM_artists': reversed(top_SE_artists), 
        'rising_SE_artists': rising_SE_artists,
        'recommended_artists': recommended_artists
    })

def leaderboards(request):
    return render_to_response('leaderboards.html',{}, context_instance=RequestContext(request))

def artist_single(request, artistname):
    example_bio = 'Coldplay is a British <a href="http://www.last.fm/tag/alternative%20rock" class="bbcode_tag" rel="tag">alternative rock</a> band, formed in London, United Kingdom in 1997. The band comprises vocalist and pianist <a href="http://www.last.fm/music/Chris+Martin" class="bbcode_artist">Chris Martin</a>, lead guitarist <a href="http://www.last.fm/music/Jonny+Buckland" class="bbcode_artist">Jonny Buckland</a>, bassist <a href="http://www.last.fm/music/Guy+Berryman" class="bbcode_artist">Guy Berryman</a>, and drummer <a href="http://www.last.fm/music/Will+Champion" class="bbcode_artist">Will Champion</a>. Having released four successful albums, (all of which debuted at #1 on the UK album chart) Coldplay have also achieved great success with their singles, such as <a title="Coldplay &ndash; Yellow" href="http://www.last.fm/music/Coldplay/_/Yellow" class="bbcode_track">Yellow</a>, <a title="Coldplay &ndash; Speed of Sound" href="http://www.last.fm/music/Coldplay/_/Speed+of+Sound" class="bbcode_track">Speed of Sound</a>, the Grammy-winning <a title="Coldplay &ndash; Clocks" href="http://www.last.fm/music/Coldplay/_/Clocks" class="bbcode_track">Clocks</a> and the US and UK #1 single <a title="Coldplay &ndash; Viva la Vida" href="http://www.last.fm/music/Coldplay/_/Viva+la+Vida" class="bbcode_track">Viva la Vida</a>. Frontman Chris Martin credits 1980s Norwegian pop band <a href="http://www.last.fm/music/a-ha" class="bbcode_artist">a-ha</a> for inspiring him to form his own band.'
    artist = type('Artist', (), {
        'name': artistname, 
        'bio': {
            'summary': example_bio
        },
        'similar': [
            {
                'name': 'Daft Punk',
                'current_price': 2200,
                'imgurls': {
                    'mega': 'http:\/\/userserve-ak.last.fm\/serve\/500\/4183432\/Daft+Punk+daftpunk_1.jpg',
                    'extralarge': 'http:\/\/userserve-ak.last.fm\/serve\/252\/4183432.jpg'    
                    # in real data, get all available image urls
                }
            },
            {
                'name': 'A random band with a missing image and a long name! (and punctuation)',
                'current_price': 100,
                'imgurls': {   
                    # in real data, get all available image urls
                }
            }
        ]
    })();
    artist_SE = type('ArtistSE', (), {
        'artist': artist,
        'ownedby': artist.name != 'Nickelback',
        'price': 2300,
        })();
    
    ##Done with the API
    # authorized_user = ttypes.AuthUser(name = request.session['user'], 
    #                   session_key = 'thekeyyougot')
    # artist_basic = client.getArtist(ttypes.Artist(mbid = '', name = 
    #                   artistname))
    # artist_se = client.getArtistSE(artist_basic, authorized_user)
    # artist_lfm = client.getArtistLFM(artist_basic)
    
    # artist = {'name':artist_basic.name, 
    #           'bio':{'summary' = artist_lfm.bio.summary}, 'similar': 
    #           artist_lfm.similar
    
    # artist_SE = {'artist': artist, 'ownedby': artist.name != 'Nickelback', 
    #              'price': artist_se.price}
    
    return render_to_response('artist_single.html', {'artist_SE': artist_SE}, context_instance=RequestContext(request))

############ Buy/Sell ############

@json_response
def sell(request, artist=None, artist_id=None, price=None):
    if (request.GET or (artist==None and artist_id==None)):
        #marketprice = se_api.get_sell_price(artist)
        marketprice = 40
        return {'marketprice': 40}
        #return render_to_response('sell.html', {'marketprice': marketprice})
    elif (request.POST):
        pass
        #TODO: Authenticate
        # if 'user' in request.session:
        #     se_api.create_sell_orders(server=server, 
        #         user=request.session['user'], price=price)

def buy_search(request):
    #TODO
    pass

def buy(request, artist=None, artist_id=None, price=None):
    #TODO
    pass

############ Helper Functions ############

def __portfolio(user=None):
    if user is not None:
        user_data = se_api.get_user_data(server=server, user=user)
        user_data.current_worth = sum(se_api.getArtistData(x).stockvalue
                            for x in user_data.curstocks)
    return user_data

def __authenticated(request):
    #if request.session['userapitoken'] is not None:
    return {}

# Close
# transport.close()
    
# except Thrift.TException, tx:
#     print '%s' % (tx.message)
