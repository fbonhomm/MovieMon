from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^TitleScreen/', views.TitleScreen, name='TitleScreen'),
    url(r'^WorldMap/', views.WorldMap, name='WordlMap'),
#    url(r'^Battle/', views.Battle, name='Battle'),
#    url(r'^Moviedex/', views.Moviedex, name='Moviedex'),
#    url(r'^Detail/', views.Detail, name='Detail'),
#    url(r'^Option/', views.Option, name='Option'),
#    url(r'^Save/', views.Save, name='Save'),
#    url(r'^Load/', views.Load, name='Load')
]
