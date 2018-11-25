from pyzombies.agents.action import Action
from pyzombies.environment.game_state import Game_State
from pyzombies.strategies.strategy import Strategy

class ZH_Strategy(Strategy):
    """"""

    def choose_if_humans(self, game_state: Game_State):
        raise NotImplementedError

    def choose_if_not_humans(self, game_state: Game_State):
        raise NotImplementedError

    def choose_from_env(self, game_state: Game_State) -> Action:
        person_map = game_state.by_type()

        if len(person_map["human"]) > 0:
            return self.choose_if_humans(game_state)
        else:
            return self.choose_if_not_humans(game_state)


