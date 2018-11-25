from pyzombies.environment.game_state import Game_State
from pyzombies.strategies.zh_strategy import ZH_Strategy
from pyzombies.agents.distance import l2_distance_btw_persons
from pyzombies.agents.action import Action

class Closest_Zombie_Strategy(ZH_Strategy):
    """"""

    def choose_if_not_humans(self, game_state: Game_State):
        zombies = game_state.by_type()["zombie"]

        allan = game_state._get_allan()

        distances = list()
        for zombie in zombies:
            distances.append(l2_distance_btw_persons(allan, zombie))

        min_dist = min(distances)

        targeted_zombie = zombies[distances.index(min_dist)]

        return Action(targeted_zombie.position)


