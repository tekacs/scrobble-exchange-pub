from django.template import RequestContext, loader
from django.http import HttpResponse
from django.shortcuts import render_to_response
import models
from utils import json_response

## Import thrift stuff

# from se_api import ScrobbleExchange
# import se_api.ttypes

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
    
    # Now you can access all the thrift stuff
    # To access methods in the ScrobbleExchange service, use
    # client.[servicename](arguments)
    # To create objects as defined in the thrift file
    # Use se_api.[ObjectName]()

def home(request):
    # user_data = __portfolio(request.session['user'])
    # user_data.worth = sum(se_api.getArtistData(x).stockvalue
    #                         for x in user_data.curstocks)
    #api_user_data = client.getUserData(request.session['user'])

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
    return render_to_response('artists.html', {'artistlist': artistlist})

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
    return render_to_response('artist_single.html', {'artist_SE': artist_SE}, context_instance=RequestContext(request))

############ Buy/Sell ############

@json_response
def price(request, artist_id=None):
    print 'entered price function correctly'
    # artist_SE = client.getArtistSE(artist = se_api.Artist(mbid = artist_id), user = request.user)
    artist_price_guarantee = client.getGuarantee(artist = se_api.Artist(mbid = artist_id), user = request.user)
    return artist_price_guarantee


@json_response
@require_POST()
def sell(request, artist=None, artist_id=None, price=None):
    #TODO: Remind Joe to check out https://docs.djangoproject.com/en/dev/ref/contrib/csrf/#ajax
    

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