from pyzombies.agents.person import Person
from pyzombies.agents.position import Position


class Zombie(Person):

    def __init__(self,
                 person_id: str,
                 position: Position
                 ):
        super(Zombie, self).__init__(person_id, position)

        self.type = "zombie"

        self.velocity = 400.
        self.attack_radius = 400.

        self.is_alive = True

    def move(self, game_state):
        self.position = self._next_position
        self._next_position = None