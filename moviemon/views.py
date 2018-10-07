import pickle

from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse

from .classes.games import Games


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

    with open(settings.BASE_SAVE + 'savefile', 'rb') as fd:
        game.load(pickle.load(fd))

    return game

def save_pickle(game):
    with open(settings.BASE_SAVE + 'savefile', 'wb') as fd:
        pickle.dump(game.dump(), fd)

def init(request):
    game = Games()
    game.load_default_settings()

    result = _information(game)

    with open(settings.BASE_SAVE + 'savefile', 'wb') as fd:
        pickle.dump(game.dump(), fd)

    return render(request, 'index.html', result)

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
    game = Games()
    game.load_default_settings()

    result = game.get_map()
    pos_x = int(request.GET.get('x')) if request.GET.get('x') else 0
    pos_y = int(request.GET.get('y')) if request.GET.get('y') else 0

#   code back here !!
#   position = "60"
#   pos_x = position.1
#   pos_y = position.0
    # if movieball is catch
    # if moviemon appear
    moviemon_id = None

    if not result['up']:
        up = '/WorldMap?x=%s&y=%s' % (str(pos_x), str(pos_y - 1))
    if not result['down']:
        down = '/WorldMap?x=%s&y=%s' % (str(pos_x), str(pos_y + 1))
    if not result['left']:
        left = '/WorldMap?x=%s&y=%s' % (str(pos_x - 1), str(pos_y))
    if not result['right']:
        right = '/WorldMap?x=%s&y=%s' % (str(pos_x + 1), str(pos_y))

    # get move possibility
    context = {
            'button': {
                'a': '/battle/' + moviemon_id,
                'start': '/moviedex',
                'select': '/option',
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
    return render(request, 'WorldMap.html', context)

def Battle(request, moviemon_id):
    movieball = 10

    context = {
            'moviemon': {
                'title': 'test',
                'id': moviemon_id,
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
