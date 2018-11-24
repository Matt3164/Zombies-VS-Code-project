from pyzombies.agents.distance import l2_distance_btw_persons
from pyzombies.agents.position import Position


class Person(object):

    def __init__(self,
                 person_id: str,
                 position: Position
                 ):
        self.position = position
        self.id = person_id

        self.velocity = None
        self.attack_radius = None

        self.is_alive = True

        self.type = None

    def move(self, game_state):
        raise NotImplementedError

    def die(self):
        self.is_alive=False

    def __repr__(self) -> str:
        return """

        I am alive

        I am {0} of type {1}

        """.format(self.id, self.type)