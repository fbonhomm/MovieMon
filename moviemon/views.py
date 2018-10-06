
from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse

from .classes.games import Games

def init(request):
  # Movies()
  Games()
  return HttpResponse('OK')
