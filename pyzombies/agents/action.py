from pyzombies.agents.position import Position


class Action(object):
    def __init__(self, position: Position):
        self._position = position

    def execute(self):
        print("{0} {1}".format(self._position.x, self._position.y))

    def __repr__(self) -> str:
        return "Action associated with {}".format(self._position)