from django.conf.urls import patterns, url

from placesreview import views


urlpatterns = patterns(
    '',
    url(r'^search_places$', views.search_places, name='search_places'),
    url(r'^add_review$', views.add_review, name='add_review'),
    url(r'^get_review$', views.get_review, name='get_review')
)
