from pyzombies.agents.action import Action
from pyzombies.agents.human import Human
from pyzombies.agents.position import Position
from pyzombies.environment.game_state import Game_State
from pyzombies.strategies.strategy import Strategy


class Allan(Human):
    def __init__(self, position: Position):
        super(Allan, self).__init__(position=position, person_id="allan")

        self.velocity = 1000
        self.attack_radius = 2000

    def decide(self, game_state: Game_State)-> Action:
        raise NotImplementedError

    def use_strategy(self, game_state: Game_State, strategy: Strategy)->Action:
        return strategy.choose_from_env(game_state)

