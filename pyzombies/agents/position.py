class Position(object):

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __repr__(self) -> str:
        return "Position : ({0}, {1})".format(self.x, self.y)