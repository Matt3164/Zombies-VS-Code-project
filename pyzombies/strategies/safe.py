from pyzombies.agents.action import Action
from pyzombies.environment.game_state import Game_State
from pyzombies.strategies.strategy import Strategy
from pyzombies.utils.optimization.ordered_multi_criteria_optimizer import Ordered_Multi_Criteria_Optimizer
from pyzombies.utils.optimization.criteria_factory import criteria_factory

class Safe_Strategy(Strategy):
    """"""

    def choose_from_env(self, game_state: Game_State) -> Action:
        dbt = game_state.distance_between_types()

        possible_actions = list()

        for human in dbt.keys():

            distances_to_zombie = [dbt[human][zombie] for zombie in dbt[human].keys()]

            min_distance = min(distances_to_zombie)

            zombie_idx = distances_to_zombie.index(min_distance)

            closest_zombie = list(dbt[human].keys())[zombie_idx]

            possible_actions.append(
                dict(distance_to_human=min_distance, zombie=closest_zombie)
            )

        opt = Ordered_Multi_Criteria_Optimizer(
            criteria_list=[
                criteria_factory('distance_to_human', "min")
            ]
        )

        selected_action = opt.find(possible_actions)

        closest_zombie = selected_action["zombie"]

        return Action(closest_zombie.position)


