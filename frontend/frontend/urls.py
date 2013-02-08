from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'frontend.views.home', name='home'),
    # url(r'^frontend/', include('frontend.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),

    url(r'^$', 'frontend.views.home', name='home'),
    url(r'^artists/', 'frontend.views.artists', name='artists'),
    url(r'^charts/', 'frontend.views.charts', name='charts'),

    # TODO: need to fix for artists with spaces in names
    url(r'^artist/(\w+)/$', 'frontend.views.artist_single', name ='artist_single'),
)
