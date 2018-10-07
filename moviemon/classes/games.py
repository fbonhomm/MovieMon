
import random
from django.conf import settings

from .movies import Movies
from .map import Map
from .players import Players

# 1 = moviemon, 2 = movieballs, 3 = rien
EVENTS = [1, 2, 3]

class Games(Movies, Map, Players):

  def __init__(self):
    self.event_current = None
    self.moviedex = list()
    Map.__init__(self, settings.MAP_HEIGHT,
                 settings.MAP_WIDTH, settings.MAP_POSITION)
    Players.__init__(self)

  def load(self, info):
    self.moviedex = info['moviedex']
    Movies.__init__(self, movies=info['moviemon'])
    Map.__init__(self, settings.MAP_HEIGHT, settings.MAP_WIDTH, info['position'])
    Players.__init__(self, len(self.moviedex) + 1, info['movieballs'])
    return self
  
  def load_default_settings(self):
    Movies.__init__(self, settings.MOVIES, settings.BASE_IMG)

    return self

  def dump(self):
    return {
      'position': self.get_position(),
      'movieballs': self.get_movieballs(),
      'moviedex': self.moviedex,
      'moviemon': self.movies
    }

  def get_moviedex(self):
    return self.moviedex
  
  def get_moviedex_full(self):
    result = list()

    for m in self.moviedex:
      result.append(self.movies[m])

    return result

  def get_random_movie(self):
    notCatch = list()

    for id in self.movies:
      if id not in self.moviedex:
        notCatch.append(id)

    return notCatch[random.randint(0, len(notCatch) - 1)]
  
  def set_catched(self, id):
    if id in self.movies:
      self.moviedex.append(id)

  def try_catch(self, id):
    if id is not self.moviedex and self.get_movieballs() > 0:
      self.movieballs_down()

      chance = self.chance_catch(id)

      rand = random.randint(0, 100)

      if rand <= chance:
        self.set_catched(id)
        return True
    
    return False
      

  def chance_catch(self, id):
    if id in self.movies:
      try:
        rating = float(self.movies[id]['rating'])
      except Exception:
        rating = 5

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
      self.event_current = EVENTS[0]
    elif idx >= 25 and idx <= 49:
      self.event_current = EVENTS[1]
    else:
      self.event_current = EVENTS[2]

    return self.event_current
  
  def get_event(self):
    return self.event_current
  
  def get_info_event(self):
    if self.event_current == 1:
      id = self.get_random_movie()

      result = self.get_movie_id(id)
      result['catchedChance'] = self.chance_catch(id)
    elif self.event_current == 2:
      self.movieballs_up()
      result = {}
    else:
      result = {}

    return result

  def isCatch(self, id):
    if id in self.moviedex:
      return True
    else:
      return False

