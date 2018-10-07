from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.TitleScreen, name='TitleScreen'),
    url(r'^worldmap', views.WorldMap, name='WordlMap'),
    url(r'^battle/(?P<id>[\w-]+)$', views.Battle, name='Battle'),
    url(r'^moviedex/((?P<id>[\w-]+)$)?', views.moviedex),
#    url(r'^Moviedex/', views.Moviedex, name='Moviedex'),
#    url(r'^Detail/', views.Detail, name='Detail'),
    url(r'^option/', views.Option, name='Option'),
#    url(r'^save/', views.Save, name='Save'),
    url(r'^options/save_game/((?P<slot>[\w-]+)$)?', views.save_game),
    url(r'^options/load_game/((?P<slot>[\w-]+)$)?', views.load_game),
]
