from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.TitleScreen, name='TitleScreen'),
    url(r'^worldmap/$', views.WorldMap, name='WordlMap'),
    url(r'^battle/(?P<id>[\w-]+)$', views.Battle, name='Battle'),
    url(r'^moviedex/((?P<id>[\w-]+)$)?', views.moviedex),
#    url(r'^Moviedex/', views.Moviedex, name='Moviedex'),
#    url(r'^Detail/', views.Detail, name='Detail'),
#    url(r'^Option/', views.Option, name='Option'),
#    url(r'^Save/', views.Save, name='Save'),
#    url(r'^Load/', views.Load, name='Load')
