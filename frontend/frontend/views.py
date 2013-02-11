from django.template import RequestContext, loader
from django.http import HttpResponse
from django.shortcuts import render_to_response

def home(request):
    return render_to_response('index.html',{})

def artists(request):
    artists = lastfm.chart.get_top_artists()
    return render_to_response('artists.html', {'artistlist': artists})

def charts(request):
    return render_to_response('charts.html',{})

def artist_single(request, artist):
    return render_to_response('artist_single.html', {'name': artist})
