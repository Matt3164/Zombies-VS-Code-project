from pyzombies.environment.game_state import Game_State
from pyzombies.strategies.closest_zombie_strategy import Closest_Zombie_Strategy
from pyzombies.agents.action import Action
from pyzombies.agents.distance import l2_distance_btw_persons
from pyzombies.utils.optimization.ordered_multi_criteria_optimizer import Ordered_Multi_Criteria_Optimizer
from pyzombies.utils.optimization.criteria_factory import criteria_factory

class Smart_Strategy(Closest_Zombie_Strategy):
    """"""

    def choose_if_humans(self, game_state: Game_State):

        zombies = game_state.by_type()["zombie"]

        humans = game_state.by_type()["human"]

        victim_humans = [human for human in humans if human.id!="allan"]

        allan = game_state._get_allan()

        possible_actions = dict()

        for zombie in zombies:

            position = zombie.position

            new_action = Action(zombie.position)

            closest_human_distance = min([l2_distance_btw_persons(zombie, human) for human in victim_humans])

            closest_human_distance_in_turns = int( (closest_human_distance- zombie.attack_radius )/zombie.velocity)

            if not (position in possible_actions.keys()):

                allan_distance = l2_distance_btw_persons(zombie, allan)

                allan_distance_in_turns = int(( allan_distance - allan.attack_radius) /allan.velocity)

                is_possible=int( ( allan_distance_in_turns - 1) <= closest_human_distance_in_turns )

                possible_actions[position] = dict(
                    action=new_action,
                    zombie_killed=1,
                    closest_human_to_zombie=closest_human_distance,
                    allan_distance=allan_distance,
                    closest_human_distance=closest_human_distance,
                    closest_human_distance_in_turns=closest_human_distance_in_turns,
                    allan_distance_in_turns=allan_distance_in_turns,
                    is_possible=is_possible
                )

            else:

                possible_actions[position]["zombie_killed"] += 1
                possible_actions[position]["closest_human_to_zombie"] = min(
                    possible_actions[position]["closest_human_to_zombie"],
                    closest_human_distance
                )
                possible_actions[position]["closest_human_distance_in_turns"] = min(
                    possible_actions[position]["closest_human_distance_in_turns"],
                    closest_human_distance
                )

                possible_actions[position]["is_possible"] = int(
                    possible_actions[position]["allan_distance_in_turns"] < possible_actions[position]["closest_human_distance_in_turns"]
                )

        opt = Ordered_Multi_Criteria_Optimizer(
            criteria_list=[
                criteria_factory('is_possible', "max"),
                criteria_factory('closest_human_distance_in_turns', "min"),
                criteria_factory('zombie_killed', "max"),
                criteria_factory('closest_human_distance', "min"),
            ]
        )

        selected_action = opt.find([item[1] for item in possible_actions.items()])

        return selected_action["action"]


