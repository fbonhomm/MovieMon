
import random
from django.conf import settings

from .movies import Movies
from .map import Map
from .players import Players


class Games(Movies, Map, Players):

  def __init__(self):
    self.moviedex = list()
    Map.__init__(self, settings.MAP_HEIGHT,
                 settings.MAP_WIDTH, settings.MAP_POSITION)
    Players.__init__(self)

  def load(self, info):
    self.moviedex = info.moviedex
    Movies.__init__(self, movies=info.moviemon)
    Map.__init__(self, settings.MAP_HEIGHT, settings.MAP_WIDTH, info.position)
    Players.__init__(self, len(self.moviedex) + 1, info.movieballs)
    return self

  def dump(self):
    return {
      'position': self.get_position(),
      'movieballs': self.get_movieballs(),
      'moviedex': self.moviedex,
      'moviemon': self.movies
    }

  def get_random_movie(self):
    notCatch = list()

    for id in self.ids:
      if id not in self.moviedex:
        notCatch.append(id)

    return notCatch[random.randint(0, len(notCatch) - 1)]

  def load_default_settings(self):
    Movies.__init__(self, settings.MOVIES, settings.BASE_IMG)

    return self

  def get_strength(self):
    return len(self.moviedex)
  
  def set_catched(self, id):
    if id in self.movies:
      self.moviedex.append(id)

  def chance_catch(self, id):
    if id in self.movies:
      rating = float(self.movies[id]['rating'])

      chance = 50 - (rating * 10) + (self.strength * 5)

      if chance < 1:
        return 1
      elif chance > 90:
        return 90
      else:
        return round(chance)
  
  def event(self):
    # 25 chance moviemon 0-24
    # 25 chance movieballs 25-49
    # 50 chance rien 40-100

    idx = random.randint(0, 100)

    if idx >= 0 and idx <= 24:
      return 'moviemon'
    elif idx >= 25 and idx <= 49:
      return 'movieball'
    else:
      return 'rien'