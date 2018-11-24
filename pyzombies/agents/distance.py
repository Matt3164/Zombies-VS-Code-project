from pyzombies.agents.position import Position
from pyzombies.agents.person import Person
from pyzombies.utils.math import l2_distance


def _l2_distance_btw_pos(pos1: Position, pos2: Position):
    return l2_distance(pos1.x, pos1.y, pos2.x, pos2.y)

def l2_distance_btw_persons(person1: Person, person2: Person):
    return _l2_distance_btw_pos(person1.position, person2.position)

