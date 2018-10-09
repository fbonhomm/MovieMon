
from players import Players

test = Players()

print(test.get_strength())
print(test.get_movieball())

test.strength_up()
test.strength_up()
test.strength_up()
test.movieballs_up()
test.movieballs_up()
test.movieballs_up()
test.movieballs_down()

print(test.get_strength())
print(test.get_movieball())
