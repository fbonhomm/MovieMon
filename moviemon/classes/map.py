

class Map:

  def __init__(self, h_case=10, w_case=10, current_case=1):
    if current_case < 1 or (w_case * h_case) < current_case:
      raise Exception('Position is not good.')
    if h_case < 1 or h_case > 100:
      raise Exception('Height is not good.')
    if w_case < 1 or w_case > 100:
      raise Exception('Width is not good.')
    else:
      self.h_case = h_case
      self.w_case = w_case
      self.current_case = current_case

  def get_position(self):
    return self.current_case

  def get_map(self):
    return {
      'position': self.current_case,
      'width': self.w_case,
      'heigth': self.h_case,
      'up': ((self.current_case - self.w_case) >= 1),
      'down': ((self.current_case + self.w_case) <= (self.w_case * self.h_case)),
      'left': ((self.current_case - 1) % self.w_case != 0),
      'right': (self.current_case % self.w_case != 0),
    }

  def move_up(self):
    if (self.current_case - self.w_case) >= 1:
      self.current_case -= self.w_case
    return self.current_case
  
  def move_down(self):
    if (self.current_case + self.w_case) <= (self.w_case * self.h_case):
      self.current_case += self.w_case
    return self.current_case
  
  def move_left(self):
    if (self.current_case - 1) % self.w_case != 0:
      self.current_case -= 1
    return self.current_case
  
  def move_right(self):
    if self.current_case % self.w_case != 0:
      self.current_case += 1
    return self.current_case
