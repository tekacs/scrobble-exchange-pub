from django.template import RequestContext, loader
from django.http import HttpResponse

def home(request):
    t = loader.get_template('index.html')
    c = RequestContext(request, {})
    return HttpResponse(t.render(c))

def artists(request):
    t = loader.get_template('artists.html')
    c = RequestContext(request, {})
    return HttpResponse(t.render(c))

def charts(request):
    t = loader.get_template('charts.html')
    c = RequestContext(request, {})
    return HttpResponse(t.render(c))

def artist_single(request, artist):
    t = loader.get_template('artist_single.html')
    c = RequestContext(request, {'name': artist})
    return HttpResponse(t.render(c))
