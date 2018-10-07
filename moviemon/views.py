
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

def TitleScreen(request):
    context = {
            'button': {
                'a': '/WorldMap',
                'b': '/load'
            },
            'event': {
                'film': 'test'
            }
    }
    return render(request, 'TitleScreen.html', context)

def WorldMap(request):
    pos_x = int(request.GET.get('x')) if request.GET.get('x') else 0
    pos_y = int(request.GET.get('y')) if request.GET.get('y') else 0


    up = '/WorldMap?x=%s&y=%s' % (str(pos_x), str(pos_y - 1))

    down ='/WorldMap?x=%s&y=%s' % (str(pos_x), str(pos_y + 1))
    left ='/WorldMap?x=%s&y=%s' % (str(pos_x - 1), str(pos_y))
    right = '/WorldMap?x=%s&y=%s' % (str(pos_x + 1), str(pos_y))

    # get move possibility
    context = {
        'button': {
            'up': up,
            'down': down,
            'left': left,
            'right': right
        },
        'grid': {
            'x': range(0,9),
            'y': range(0,9)
        },
        'player': (pos_y, pos_x)
    }
    print(context)
    return render(request, 'WorldMap.html', context)
