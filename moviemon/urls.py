
from django.conf.urls import url
from django.urls import re_path

from moviemon import views

urlpatterns = [
  url(r'^$', views.init),
  url(r'^worldmap', views.worldmap),
  url(r'^moviedex/((?P<id>[\w-]+)$)?', views.moviedex),
  url(r'^battle/(?P<id>[\w-]+)$', views.battle),
  url(r'^options$', views.options),
  url(r'^options/save_game/((?P<slot>[\w-]+)$)?', views.save_game),
  url(r'^options/load_game/((?P<slot>[\w-]+)$)?', views.load_game),
]
