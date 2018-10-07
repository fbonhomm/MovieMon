
from django.conf.urls import url
from django.urls import re_path

from moviemon import views

urlpatterns = [
  url(r'^$', views.init),
  url(r'^move', views.move),
  re_path(r'^worldmap', views.worldmap),
  re_path(r'^moviedex/((?P<id>[\w-]+)$)?', views.moviedex),
  re_path(r'^battle/(?P<id>[\w-]+)$', views.battle),
]
