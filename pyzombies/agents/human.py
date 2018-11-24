from pyzombies.agents.person import Person
from pyzombies.agents.position import Position


class Human(Person):

    def __init__(self,
                 person_id: str,
                 position: Position
                 ):
        super(Human, self).__init__(person_id, position)

        self.type = "human"

        self.velocity = 0.
        self.attack_radius = 0.

        self.is_alive = True