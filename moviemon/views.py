
import os
import pickle

from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse
from django.http import Http404

from .classes.games import Games

def position(width, position):
    pos = int(position / width)
    if position % width == 0:
        pos1 = width
    else:
        pos1 = int(position % width)
    return (pos, pos1)

# -------------- PRIVATE --------------
def _information_savefile(game):
  result = _information(game)
  result['saves'] = {'a': {}, 'b': {}, 'c': {}}
  list_dirs = os.listdir(settings.BASE_SAVE)

  for d in list_dirs:
    with open(settings.BASE_SAVE + d, 'rb') as fd:
      file = pickle.load(fd)

      result['saves'][file['name']] = {
          'moviedex': len(file['moviedex']),
          'moviemon': len(file['moviemon']),
      }

      fd.close()
  return result


def _information(game, id=None):
  result = game.get_map()
  result['movieballs'] = game.get_movieballs()
  result['strength'] = game.get_strength()
  result['moviedex_nb'] = len(game.get_moviedex())

  if id is not None:
    result['info_event'] = game.get_movie_id(id)
  else:
    result['info_event'] = game.get_info_event()

  return result


def _load_pickle():
  game = Games()

  with open(settings.BASE_TMP + 'savefile', 'rb') as fd:
    game.load(pickle.load(fd))
    fd.close()

  return game


def _save_pickle(game):
  with open(settings.BASE_TMP + 'savefile', 'wb') as fd:
    pickle.dump(game.dump(), fd)
    fd.close()


# -------------- PUBLIC --------------
def init(request):
  game = Games()
  game.load_default_settings()

  result = _information(game)

  _save_pickle(game)
  
  context = {
            'button': {
                'a': '/worldmap',
                'b': '/load',
                'start': '/moviedex',
                'select': '/option'
            },
            'event': {
                'film': 'test'
            }
        }
  return render(request, 'TitleScreen.html', context)


def option(request):
  
  game = _load_pickle()

  result = _information(game)
  context = {
          'button': {
              'a': '/save_game',
              'b': '/',
              'start': '/worldmap',
          }
      }
  
  _save_pickle(game)
  
  return render(request, 'Options.html', context)


def WorldMap(request):
    game = load_pickle()

    if 'direction' in request.GET:
        moved = False
    
        if request.GET['direction'] == 'left':
            moved = game.move_left()
        if request.GET['direction'] == 'right':
            moved = game.move_right()
        if request.GET['direction'] == 'down':
            moved = game.move_down()
        if request.GET['direction'] == 'up':
            moved = game.move_up()
        
        if moved == True:
            evt = game.event()
        else:
            evt = game.get_event()
        
        result = _information(game)
        result['event'] = evt
        print("information:", result)
        
        save_pickle(game)
    else:
        result = _information(game)

    print("information1:", result)

    up = '/worldmap?direction=up&first=true' if result['up'] else '/worldmap?first=true'
    down = '/worldmap?direction=down&first=true' if result['down'] else '/worldmap?first=true'
    left = '/worldmap?direction=left&first=true' if result['left'] else '/worldmap?first=true'
    right = '/worldmap?direction=right&first=true' if result['right'] else '/worldmap?first=true'

    player_yx = position(result['width'], result['position'])

    a = ''
    event_text =''
    if result.get('event') and result['event'] == 1:
        a = '/battle/' + result['info_event']['id']
        event_text = "You encounter a moviemon"
    if result.get('event') and result['event'] == 2:
        event_text = "You catch a movieball"

    # get move possibility
    context = {
            'button': {
                'a': a,
                'start': '/moviedex',
                'select': '/option',
                'up': up,
                'down': down,
                'left': left,
                'right': right
            },
            'grid': {
                'x': range(1, result['width']),
                'y': range(1, result['heigth'])
            },
            'player': {
                'y': player_yx[0],
                'x': player_yx[1],
                'strength': result['strength'],
                'movieballs': result['movieballs'],
                'moviedex_nb': result['moviedex_nb']
            },
            'event': event_text
        }
    print(context)
    return render(request, 'WorldMap.html', context)


def moviedex(request):
  game = _load_pickle()

  result = _information(game)

  movie = None
  id = request.GET['id'] if 'id' in request.GET else None
  result['moviedex'] = game.get_moviedex()

  if (id and game.isExisting(id) == False) or (id and game.isCatch(id) == False):
    raise Http404('Id not conform.')

  if id is not None:
    for idx, m in enumerate(result['moviedex']):
      if id == m:
        movie = m
        prev = ('/moviedex?id=' + result['moviedex'][idx - 1]) if (idx - 1) >= 0 else '/moviedex'
        suiv = ('/moviedex?id=' + result['moviedex'][idx + 1]) if (idx + 1) < len(result['moviedex']) else '/moviedex?id=' + result['moviedex'][idx]
        break
  else:
    movie = result['moviedex'][:1][0] if len(result['moviedex'][:1]) > 0 else None
    prev = ''
    suiv = ('/moviedex?id=' + result['moviedex'][1:2][0]) if len(result['moviedex'][1:2]) > 0 else ''

  context = {
    'button': {
      'a': ('/moviedex/' + str(movie)) if movie is not None else '/moviedex',
      'select': '/worldmap',
      'left': prev,
      'right': suiv
    },
    'data': {
      'moviemon_id': movie if movie else None,
    },
    'event': {
      'film': 'test'
    }
  }

  _save_pickle(game)

  return render(request, 'MovieDex.html', context)


def moviedex_id(request, id=None):
  game = _load_pickle()

  result = _information(game)

  if id and game.isExisting(id) and game.isCatch(id) is True:
    result['details'] = game.get_movie_id(id)
    context = {
        'button': {
          'b': '/moviedex',
        },
        'data': {
          'details': result['details'] if 'details' in result else None
        },
        'event': {
          'film': 'test'
        }
    }

    _save_pickle(game)

    return render(request, 'MovieDex.html', context)
  raise Http404('Id not conform.')


def battle(request, id=None):
  game = _load_pickle()
  context = _information(game, id)

  if id and game.isExisting(id):
    if game.isCatch(id) is True:
      context['info_event']['text'] = ''
      context['button'] = {
        'a': '/worldmap',
        'b': '/worldmap'
      }
    elif game.get_movieballs() <= 0:
      context['info_event']['text'] = 'Ha les boules, il n\'a plus de movieballs'
      context['button'] = {
        'a': '/worldmap',
        'b': '/worldmap'
      }
    elif 'first' not in request.GET:
      catched = game.try_catch(id)
      context['info_event']['text'] = 'Oui je l\'ai eu !!!' if catched == True else 'HAAA j\'ai louper mon coup'
      context['button'] = {
        'a': '/worldmap' if catched == True else '/battle/' + id,
        'b': '/worldmap'
      }
    else:
      context['info_event']['text'] = 'haut les mains voyous'
      context['button'] = {
        'a': '/battle/' + id,
        'b': '/worldmap'
      }
    
    _save_pickle(game)

    return render(request, 'Battle.html', context)
  raise Http404('Id not conform.')


def options(request):
  return HttpResponse('OK')


def save_game(request, slot=None):
  game = _load_pickle()
  loaded = False

  if not os.path.exists(settings.BASE_SAVE):
    os.makedirs(settings.BASE_SAVE)

  list_dirs = os.listdir(settings.BASE_SAVE)

  if slot is not None and slot not in ['a', 'b', 'c']:
    raise Http404('Slot not conform.')

  if slot is not None and slot in ['a', 'b', 'c']:
    nb_moviedex = len(game.get_moviedex())
    nb_moviemon = len(game.get_movie())
    new_name = settings.BASE_SAVE + 'slot' + slot + \
        '_' + str(nb_moviedex) + '_' + str(nb_moviemon)

    for d in list_dirs:
      if slot == d[4:5]:
        os.rename(settings.BASE_SAVE + d, new_name)

    with open(new_name, 'wb') as fd:
      result = game.dump()
      result['name'] = slot
      pickle.dump(result, fd)
      fd.close()
      loaded = True
    

  # information on slots
  result = _information_savefile(game)
  result['saves_route'] = 'save_game'
  result['loaded'] = loaded
  _save_pickle(game)

  return render(request, 'Load.html', result)


def load_game(request, slot=None):
    game = load_pickle()
    loaded = False

    if 'select' in request.GET:
        select = request.GET['select']
    else:
        select = 'a'
    
    if not os.path.exists(settings.BASE_SAVE):
      os.makedirs(settings.BASE_SAVE)
    
    list_dirs = os.listdir(settings.BASE_SAVE)
    
    if slot is not None and slot in ['a', 'b', 'c']:
      for d in list_dirs:
        if slot == d[4:5]:
          with open(os.path.join(settings.BASE_SAVE, d), 'rb') as fd:
            game.load(pickle.load(fd))
            fd.close()
            loaded = True
    
    # information on slots
    result = _information_savefile(game)
    result['loaded'] = loaded
    _save_pickle(game)

    if select == 'a':
        up = 'c'
        down = chr(ord('a') + 1)
    elif select == 'c':
        up = chr(ord('c') - 1)
        down = 'a'
    else:
        up = chr(ord(select) - 1)
        down = chr(ord(select) + 1)

    context = {
            'button': {
                'up': '/options/load_game/?select=' + up,
                'down': '/options/load_game/?select=' + down,
                'a': '/options/load_game/' + select if select else '',
                'b': '/',
                'start': '/worldmap',
            },
            'select': select,
            'saves': result['saves']
        }
    return render(request, 'Load.html', context)
