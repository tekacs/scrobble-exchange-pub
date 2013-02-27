from django.template import RequestContext, loader
from django.http import HttpResponse
from django.shortcuts import render_to_response, redirect
from django.views.decorators.http import require_POST
from django import forms
from django.conf import settings
from django.core.urlresolvers import reverse

import models
from utils import json_response
from se_api import ttypes

import random
from urllib import quote

RESULTS_PER_PAGE = 9;
client = settings.CLIENT
TIME_RANGE_TRANSLATION = [0,31,7,1]
#TODO: Handle exceptions with the client

def home(request):
    #Done with the API
    if request.user_is_authenticated:
        authorized_user = __authuser(request)

        api_user_data = client.getUserData('fiwl')
        
        user_data = models.UserData()
        user_data.stocks = []
        
        for artistse in api_user_data.stocks:
            a = {'name': artistse.artist.name, 'imgurls': 
                                                        artistse.artist.imgurls}
            user_data.stocks.append({'artist': a, 'price': artistse.price,
                            'points': artistse.price, 'dividend':artistse.dividend})
            
        user_data.user = {'money': client.getUserMoney(authorized_user).money, 
                        'points': api_user_data.user.points}
        user_data.portfolio_worth = sum(artist.price for artist in 
                                                        api_user_data.stocks)

        return render_to_response('index.html',
            {'user_data': user_data}, context_instance=RequestContext(request)
            )
    else:
        return render_to_response('index.html', {}, context_instance=RequestContext(request))

def user_profile(request, username):
    return render_to_response('user_profile.html',{}, context_instance=RequestContext(request))

############ Leaderboards ############
'''By default, show leaderboard that the user is on. Retrieve other leaderboards user requests via AJAX'''
def leaderboards(request):
    return render_to_response('leaderboards.html',{}, context_instance=RequestContext(request))

'''Sample URL: http://localhost:8000/leaderboards/get/user?time_range=3'''
@json_response
def get_user_leaderboard(request):
    #given: time_range (0-3, 0-alltime, 1-month, 2-week, 3-day)
    unsafe_time_range = int(request.GET.get('time_range', '2'))
    if (unsafe_time_range < len(TIME_RANGE_TRANSLATION)):
        time_range = TIME_RANGE_TRANSLATION[unsafe_time_range]
    else:
        time_range = TIME_RANGE_TRANSLATION[2]

    userdata = client.getUserData(request.user.username)

    user_league = userdata.league.__dict__
    user_points = userdata.user.points

    userleaderboard = client.getNearUsers(request.user.username)
    #TODO: Remove magic number and use current position of user instead
    if (userleaderboard.users[3]):
        next_user = userleaderboard.users[3].__dict__
    else:
        next_user = {}

    user_position = userleaderboard.position

    data = {
        'user_league':user_league, 
        'user_points': user_points, 
        'user_position': user_position, 
        'next_user': next_user
    }

    return data

'''See http://localhost:8000/leaderboards/get/?league_id=1&time_range=3 for example'''
@json_response
def get_leaderboard(request):
    
    league_id = request.GET.get('league_id','default_league')
    time_range = TIME_RANGE_TRANSLATION[int(request.GET.get('time_range', '2'))]
    
    # none of the below values make any difference with dummy data 
    #TODO: Replace magic number for default users
    board = client.getTopUsers(n=100, league = ttypes.League(name=league_id), 
    trange = time_range)
    
    aadata = []
    for i in range(len(board.users)):
        aa = {
            '0': str(i+1),
            '1': '<a hred = "#"><img src=\"http://lorempixel.com/48/48/\">'\
            +board.users[i].name+'</a>',
            '2': str(board.users[i].points),
            'DT_RowClass': 'place-'+str(i+1)
        }
        
        aadata.append(aa)
        
    leaderboard = {
        'sEcho': 1,
        'iTotalRecords': '50',
        'iTotalDisplayRecords': '50',
        'aaData': aadata
    }
    
    return leaderboard


############ Artist stuff ############
def artists(request):
    authorized_user = __authuser(request)
    artist1 = ttypes.Artist(name = 'Iron Maiden')
    artist2 = ttypes.Artist(name = 'Foo Fighters')
    artistlist = [artist1, artist2]

    api_top_artists = client.getSETop(5, 5)
    top_SE_artists = []
    for i in api_top_artists:
        a = client.getArtistSE(i, authorized_user)
        artist = {'name': i.name, 'imgurls': i.imgurls}
        top_SE_artists.append({'artist':artist, 'price': a.price, 'points': 
        a.points})
    
    rising_SE_artists = list(top_SE_artists)
    random.shuffle(rising_SE_artists)
    
    recommended_artists = list(top_SE_artists)
    random.shuffle(recommended_artists)
    
    popular_LFM_artists = list(top_SE_artists)
    random.shuffle(popular_LFM_artists)
    
    recently_traded_artists = list(top_SE_artists)
    random.shuffle(recently_traded_artists)

    return render_to_response('artists.html', {
        'artistlist': artistlist,
        'top_SE_artists': top_SE_artists,
        'top_traded_artists': reversed(top_SE_artists),
        'popular_LFM_artists': popular_LFM_artists,
        'recommended_artists': recommended_artists,
        'recently_traded_artists': recently_traded_artists
    })

def artist_single(request, artistname):
    #TODO: Fix bio
    #TODO: Change artist name mechanism, look at http://stackoverflow.com/a/837835/181284
    if (artistname == ''):
        return redirect('artists')
    authorized_user = __authuser(request)
    artist_basic = client.getArtist(ttypes.Artist(mbid = '', name = 
                    artistname))
    artist_se = client.getArtistSE(artist_basic, authorized_user)
    artist_lfm = client.getArtistLFM(artist_basic, authorized_user)
    
    artist = {'name':artist_basic.name, 
            'bio':{'summary': artist_lfm.bio.summary}, 'similar': 
            artist_lfm.similar}
    
    artist_sse = {'artist': artist, 'ownedby': artist_se.ownedby, 
                'price': artist_se.price, 'points': artist_se.points, 
                'dividends': artist_se.dividend}

    return render_to_response('artist_single.html', {
        'artist_SE':artist_sse}, context_instance=RequestContext(request))

''' Sample URL: http://127.0.0.1:8000/artist/history/?artist_id=0383dadf-2a4e-4d10-a46a-e9e041da8eb3&days=2'''
@json_response
def artist_history(request):
    # artist_id = request.GET.get('artist_id')
    # artist = ttypes.Artist(mbid=artist_id)

    # days = int(request.GET.get('days', '1'))

    # history = client.getArtistHistory(artist, days)

    field = request.GET.get('field', 'money')

    if (field == 'money'):
        history = [
            {
                "name": "price",
                "data": [ { "x": 0, "y": 40 }, { "x": 1, "y": 49 }, { "x": 2, "y": 38 }, { "x": 3, "y": 30 }, { "x": 4, "y": 32 } ]
            }, {
                "name": "dividends",
                "data": [ { "x": 0, "y": 19 }, { "x": 1, "y": 22 }, { "x": 2, "y": 29 }, { "x": 3, "y": 20 }, { "x": 4, "y": 14 } ]
            }
        ]
    elif (field == 'points'):
        history = [
            {
                "name": "points",
                "data": [ { "x": 0, "y": 30 }, { "x": 1, "y": 13 }, { "x": 2, "y": 35 }, { "x": 3, "y": 50 }, { "x": 4, "y": 42 } ]
            }
        ]
    return history

''' Sample URL: http://localhost:8000/search/autocomplete/?q=blah '''
@json_response
def auto_complete(request):
    #TODO: Change format of data
    partial_text = request.GET.get('q','')
    results = client.searchArtist(partial_text, RESULTS_PER_PAGE, 1)
    
    auto = []
    for a in results:
        adict = {
            'value': a.name,
            'url': quote('/artist/'+a.name),
        }
        try:
            adict['img'] = a.imgurls['mega']
        except KeyError:
            pass
        
        auto.append(adict)
        
    return auto

''' Sample URL: http://localhost:8000/search/?q=blah . See https://docs.djangoproject.com/en/dev/topics/forms/ '''
def search(request):
    query = request.GET.get('q','')
    if (query == ''):
        return render_to_response('search_results.html', {
            'query' : '',
            'results' : {},
            'page' : 1,
            'next_page' : "#",
            'previous_page' : "#"
            }, context_instance=RequestContext(request))

    page_number = int(request.GET.get('page', '1'))

    if (page_number > 1):
        previous_page = "%s?q=%s&page=%s" % (reverse('frontend.views.search'), query, page_number - 1)
    else:
        previous_page = "#"
    next_page = "%s?q=%s&page=%s" % (reverse('frontend.views.search'), query, page_number + 1)


    results = client.searchArtist(query, RESULTS_PER_PAGE, page_number)
    if (request.GET.get('lucky', 'false') == 'true' and results):
        #TODO: Pass ID instead of name once artist_single can handle it
        return redirect('artist_single', results[0].name)
    else:
        return render_to_response('search_results.html', {
            'query':query,
            'results': results,
            'page':page_number,
            'next_page':next_page,
            'previous_page':previous_page}, context_instance=RequestContext(request))


############ Buy/Sell ############

@json_response
def price(request, artist_id=None):
    # artist_name = request.GET.get('artist_name')
    artist = ttypes.Artist(name = artist_name)
    authuser =  __authuser(request)
    # artist_SE = client.getArtistSE(artist = artist, user = authuser)
    # TODO: Ask Victor why this may be throwing exceptions
    # Throws errors because the test backend currently only looks stuff up by 
    # artist name
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
    artist = ttypes.Artist(mbid = artist_id)
    artist_price_guarantee = client.getGuarantee(artist = artist, user = __authuser(request)).__dict__
    return artist_price_guarantee

@json_response
@require_POST
def sell(request):
    #TODO: Remind Joe to check out https://docs.djangoproject.com/en/dev/ref/contrib/csrf/#ajax
    # guarantee = request.POST.get('guarantee')
    elephant = request.POST.get('elephant')
    price = int(request.POST.get('price'))
    time = int(request.POST.get('time'))
    artist = ttypes.Artist(mbid=request.POST.get('artist_id')

    guarantee = ttypes.Guarantee(elephant = elephant, artist = artist, price = price, time = time)

    success = client.sell(guarantee=guarantee, user=__authuser(request))
    return success;

@json_response
@require_POST
def buy(request):
    elephant = request.POST.get('elephant')
    price = int(request.POST.get('price'))
    time = int(request.POST.get('time'))
    artist = ttypes.Artist(mbid=request.POST.get('artist_id')

    guarantee = ttypes.Guarantee(elephant = elephant, artist = artist, price = price, time = time)

    success = client.buy(guarantee=guarantee, user=__authuser(request))
    return success;


############ Helper Functions ############

def __portfolio(user=None):
    if user is not None:
        user_data = se_api.get_user_data(server=server, user=user)
        user_data.current_worth = sum(se_api.getArtistData(x).stockvalue
                            for x in user_data.curstocks)
    return user_data

def __authuser(request):
    return ttypes.AuthUser(name=ttypes.User(request.user.username), session_key=request.user.first_name)

class ArtistSearchForm(forms.Form):
    q = forms.CharField(max_length=100, label='Query: ')
