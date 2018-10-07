
import os
import pickle

from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse

from .classes.games import Games

def position(width, position):
    pos = int(position / width)
    if position % width == 0:
        pos1 = width
    else:
        pos1 = int(position % width)
    return (pos, pos1)

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


def load_pickle():
  game = Games()

  with open(settings.BASE_TMP + 'savefile', 'rb') as fd:
    game.load(pickle.load(fd))
    fd.close()

  return game

def save_pickle(game):
  with open(settings.BASE_TMP + 'savefile', 'wb') as fd:
    pickle.dump(game.dump(), fd)
    fd.close()


def init(request):
  game = Games()
  game.load_default_settings()

  result = _information(game)

  save_pickle(game)

def Option(request):
    context = {
            'button': {
                'a': '/save',
                'b': '/',
                'start': '/worldmap',
            }
        }
    return render(request, 'Options.html', context)

def Load():
    game = Games()

    with open(settings.BASE_SAVE + 'savefile', 'rb') as fd:
        game.load(pickle.load(fd))

    return game

def TitleScreen(request):
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

def Battle(request, id):
    movieball = 10
    context = {
            'moviemon': {
                'title': 'test',
                'id': id,
            },
            'player': {
                'movieball': movieball
            },
            'event': {
                'text': 'Moviemon has appear !!!'
            }
        }
    return render(request, 'Battle.html', context)

def move(request):
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
        
        save_pickle(game)
        
        return render(request, 'index.html', result)
    return HttpResponse('Direction not set.')

def worldmap(request):
  game = load_pickle()

  result = _information(game)

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

  save_pickle(game)

  return render(request, 'index.html', result)


def moviedex(request, id):
  game = load_pickle()

  result = _information(game)

  print(id)
  if id and game.isExisting(id) and game.isCatch(id) is True:
    result['details'] = game.get_movie_id(id)
  else:
    result['moviedex'] = game.get_moviedex()

  save_pickle(game)

  return render(request, 'index.html', result)


def battle(request, id):
  game = load_pickle()

  if id and game.isCatch(id) is False:

    result = _information(game, id)
    result['info_event']['catched'] = game.try_catch(id)

    save_pickle(game)

    return render(request, 'index.html', result)
  return HttpResponse('Id not conform.')


def options(request):
  return HttpResponse('OK')


def save_game(request, slot=None):
  game = load_pickle()

  if not os.path.exists(settings.BASE_SAVE):
    os.makedirs(settings.BASE_SAVE)

  list_dirs = os.listdir(settings.BASE_SAVE)

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

  # information on slots
  result = _information_savefile(game)
  result['saves_route'] = 'save_game'
  save_pickle(game)

  return render(request, 'index.html', result)


def load_game(request, slot=None):
  game = load_pickle()

  if not os.path.exists(settings.BASE_SAVE):
    os.makedirs(settings.BASE_SAVE)

  list_dirs = os.listdir(settings.BASE_SAVE)

  if slot is not None and slot in ['a', 'b', 'c']:
    for d in list_dirs:
      if slot == d[4:5]:
        with open(os.path.join(settings.BASE_SAVE, d), 'rb') as fd:
          game.load(pickle.load(fd))
          fd.close()

  # information on slots
  result = _information_savefile(game)
  result['saves_route'] = 'load_game'
  save_pickle(game)

  return render(request, 'index.html', result)
