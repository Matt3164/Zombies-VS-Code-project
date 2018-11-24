from pyzombies.agents.action import Action
from pyzombies.agents.allan import Allan
from pyzombies.environment.game_state import Game_State


class Safe_Allan(Allan):

    def decide(self, game_state: Game_State)-> Action:

        dbt = game_state.distance_between_types()

        possible_actions = list()

        for human in dbt.keys():

            distances_to_zombie = [ dbt[human][zombie] for zombie in dbt[human].keys() ]

            min_distance = min(distances_to_zombie)

            zombie_idx = distances_to_zombie.index(min_distance)

            closest_zombie = list(dbt[human].keys())[zombie_idx]

            possible_actions.append(
                dict(distance_to_human=min_distance, zombie=closest_zombie)
            )

        distances = [poss_action["distance_to_human"] for poss_action in possible_actions]

        min_distance = min(distances)

        zombie_idx = distances.index(min_distance)

        closest_zombie = possible_actions[zombie_idx]["zombie"]

        return Action(closest_zombie.position)