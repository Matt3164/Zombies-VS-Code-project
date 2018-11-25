from pyzombies.environment.game_state import Game_State
from pyzombies.agents.action import Action

class Strategy(object):
    """"""

    def __init__(self):
        """Constructor for Strategy"""
        pass

    def choose_from_env(self, game_state: Game_State)->Action:
        raise NotImplementedError

