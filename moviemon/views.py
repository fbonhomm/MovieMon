
from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse

from .classes.games import Games

def init(request):
  game = Games()
  game.load_default_settings()

  return HttpResponse('OK')
