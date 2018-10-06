
from django.conf.urls import url

from moviemon import views

urlpatterns = [
  url(r'^$', views.init),
]
