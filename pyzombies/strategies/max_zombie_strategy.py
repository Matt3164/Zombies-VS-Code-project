from pyzombies.environment.game_state import Game_State
from pyzombies.strategies.closest_zombie_strategy import Closest_Zombie_Strategy
from pyzombies.agents.action import Action
from pyzombies.agents.distance import l2_distance_btw_persons
from pyzombies.utils.optimization.ordered_multi_criteria_optimizer import Ordered_Multi_Criteria_Optimizer
from pyzombies.utils.optimization.criteria_factory import criteria_factory

class Max_Zombie_Strategy(Closest_Zombie_Strategy):
    """"""

    def choose_if_humans(self, game_state: Game_State):

        zombies = game_state.by_type()["zombie"]

        humans = game_state.by_type()["human"]

        possible_actions = dict()

        for zombie in zombies:

            position = zombie.position

            new_action = Action(zombie.position)

            closest_human_distance = min([l2_distance_btw_persons(zombie, human) for human in humans])

            if not (position in possible_actions.keys()):

                possible_actions[position] = dict(
                    action=new_action,
                    zombie_killed=1,
                    closest_human_to_zombie=closest_human_distance
                )

            else:

                possible_actions[position]["zombie_killed"] += 1
                possible_actions[position]["closest_human_to_zombie"] = min(
                    possible_actions[position]["closest_human_to_zombie"],
                    closest_human_distance
                )

        opt = Ordered_Multi_Criteria_Optimizer(
            criteria_list=[
                criteria_factory('zombie_killed', "max"),
                criteria_factory('closest_human_to_zombie', "min")
            ]
        )

        selected_action = opt.find([item[1] for item in possible_actions.items()])

        return selected_action["action"]


