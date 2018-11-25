from pyzombies.agents.action import Action
from pyzombies.agents.position import Position
from pyzombies.environment.game_state import Game_State
from pyzombies.strategies.strategy import Strategy
from pyzombies.environment.key_figures import HEIGHT, WIDTH
import random # needed


class Dumb_Strategy(Strategy):
    """"""

    def choose_from_env(self, game_state: Game_State) -> Action:

        random_position = Position(
            random.randint(0, WIDTH),
            random.randint(0, HEIGHT)
        )

        return Action( position=random_position )
