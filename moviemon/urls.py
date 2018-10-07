from django.conf.urls import url
from . import views

urlpatterns = [
    url('/', views.TitleScreen, name='TitleScreen'),
    url(r'^worldmap/$', views.WorldMap, name='WordlMap'),
    url(r'^Battle/(?P<moviemon_id>[0-9]+)/$', views.Battle, name='Battle'),
#    url(r'^Moviedex/', views.Moviedex, name='Moviedex'),
#    url(r'^Detail/', views.Detail, name='Detail'),
#    url(r'^Option/', views.Option, name='Option'),
#    url(r'^Save/', views.Save, name='Save'),
#    url(r'^Load/', views.Load, name='Load')
]
