
from map import Map

test = Map()

print(test.get_map())


test.move_down()
test.move_right()
test.move_right()
test.move_right()
test.move_down()

print(test.get_map())

test = Map(current_case=200)
