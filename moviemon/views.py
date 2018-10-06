
import pickle

from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse

from .classes.games import Games

def init(request):
  game = Games()
  game.load_default_settings()

  result = game.get_map()
  result['movieballs'] = game.get_movieballs()
  result['event'] = game.event()

  with open(settings.BASE_SAVE + 'savefile', 'wb') as fd:
    pickle.dump(game.dump(), fd)

  return render(request, 'index.html', result)

# def move(request):
