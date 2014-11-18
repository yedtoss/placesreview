from django.conf.urls import patterns, include, url

from django.contrib import admin
from placesreview import views
#admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mashtaton.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    #url(r'^admin/', include(admin.site.urls)),
    url(r'^search_places$', views.search_places, name='search_places'),
    url(r'^add_review$', views.add_review, name='add_review'),
    url(r'^get_review$', views.get_review, name='get_review')
)
