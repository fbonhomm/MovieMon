
class Players:

  def __init__(self, strength=1, movieballs=1):
    self.strength = strength
    self.movieballs = movieballs

  def get_strength(self):
    return self.strength
  
  def get_movieballs(self):
    return self.movieballs

  def strength_up(self):
    self.strength += 1
  
  def movieballs_up(self):
    self.movieballs += 1
  
  def movieballs_down(self):
    if self.movieballs > 0:
      self.movieballs -= 1
