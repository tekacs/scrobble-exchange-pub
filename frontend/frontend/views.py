from django.template import RequestContext, loader
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.views.decorators.http import require_POST
from django import forms

import models
from utils import json_response

import random

RESULTS_PER_PAGE = 10;

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

    return render_to_response('artists.html', {
        'artistlist': artistlist,
        'top_SE_artists': top_SE_artists,
        'top_LFM_artists': reversed(top_SE_artists),
        'rising_SE_artists': rising_SE_artists,
        'recommended_artists': recommended_artists
    })

############ Leaderboards ############
'''By default, show leaderboard that the user is on. Retrieve other leaderboards user requests via AJAX'''
def leaderboards(request):
    # leaderboard = client.getNearUsers(request.user)
    userleaderboard = {}
    return render_to_response('leaderboards.html',{'leaderboard': userleaderboard}, context_instance=RequestContext(request))

'''See http://localhost:8000/leaderboards/get/?league_id=1&time_range=3 for example'''
@json_response
def get_leaderboard(request):
    league_id = request.GET.get('league_id','default_league')
    time_range = request.GET.get('time_range', 'default_time_range')
    # leaderboard = client.getTopUsers(RESULTS_PER_PAGE, league_id, time_range)

    # Data must be in this format to work with jQuery datatables library, need to craft json into this format
    leaderboard = {
        "sEcho": 1,
        "iTotalRecords": "50",
        "iTotalDisplayRecords": "50",
        "aaData":[
            {
                "0": "1",
                "1": "<a href=\"#\"><img src=\"http://lorempixel.com/48/48/\"> neil-s</a>",
                "2": "70",
                "DT_RowClass": "place-1"
            },
            {
                "0": "2",
                "1": "<a href=\"#\"><img src=\"http://lorempixel.com/48/48/\"> joebateson</a>",
                "2": "40",
                "DT_RowClass": "place-2 me"
            },
            {
                "0": "3",
                "1": "<a href=\"#\"><img src=\"http://lorempixel.com/48/48/\"> rand</a>",
                "2": "20",
                "DT_RowClass": "place-3"
            }
        ]
    }
    return leaderboard


############ Artist stuff ############
def artist_single(request, artistname):
    #TODO: Change artist name mechanism
    example_bio = """Coldplay is a British <a
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


''' Sample URL: http://localhost:8000/search/autocomplete/?q=blah '''
@json_response
def auto_complete(request):
    partial_text = request.GET.get('q')
    # results = client.searchArtist(partial_text)
    results = {}
    return results

''' Sample URL: http://localhost:8000/search/?q=blah . See https://docs.djangoproject.com/en/dev/topics/forms/ '''
def search(request):
    results = {}
    if request.method == 'POST': # If the form has been submitted...
        form = ArtistSearchForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            results = client.searchArtist(form.cleaned_data['q'])
            if (request.POST.get('lucky', 'false') == true):
                #TODO: Pass ID instead of name once artist_single can handle it
                return redirect('artist_single', artistname=results[0].name)
    else:
        form = ArtistSearchForm() # An unbound form

    return render_to_response('search_results.html', {
        'form': form, 'results': results}, context_instance=RequestContext(request))


############ Buy/Sell ############

@json_response
def price(request, artist_id=None):
    # artist_SE = client.getArtistSE(artist = se_api.Artist(mbid = artist_id), user = request.user)
    artist_SE = {
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
    }
    return artist_SE

@json_response
def guaranteed_price(request):
    artist_id = request.GET.get('artist_id')
    artist_price_guarantee = client.getGuarantee(artist = se_api.Artist(mbid = artist_id), user = request.user)
    return artist_price_guarantee

@json_response
@require_POST
def sell(request):
    #TODO: Remind Joe to check out https://docs.djangoproject.com/en/dev/ref/contrib/csrf/#ajax
    guarantee = request.POST.get('guarantee')  
    success = client.sell(guarantee=se_api.Guarantee(guarantee), user=se_api.AuthUser(request.user))
    return success;

@json_response
@require_POST
def buy(request):
    guarantee = request.POST.get('guarantee')  
    success = client.buy(guarantee=se_api.Guarantee(guarantee), user=se_api.AuthUser(request.user))
    return success;


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

class ArtistSearchForm(forms.Form):
    q = forms.CharField(max_length=100, label='Query: ')
