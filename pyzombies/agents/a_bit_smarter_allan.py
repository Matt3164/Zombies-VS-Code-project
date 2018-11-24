from pyzombies.agents.action import Action
from pyzombies.agents.allan import Allan
from pyzombies.environment.game_state import Game_State
from pyzombies.agents.distance import l2_distance_btw_persons


class A_Bit_Smarter_Allan(Allan):

    def decide_if_humans(self, game_state: Game_State):

        zombies = game_state.by_type()["zombie"]

        humans = game_state.by_type()["zombie"]

        possible_actions = dict()

        for zombie in zombies:

            position = zombie.position

            new_action = Action(zombie.position)

            closest_human_distance = min([l2_distance_btw_persons(zombie, human) for human in humans])

            if not ( position in possible_actions.keys()):

                possible_actions[position] = dict(
                    action=new_action,
                    zombie_killed=1,
                    closest_human_to_zombie=closest_human_distance
                )

            else:

                possible_actions[position]["zombie_killed"]+=1
                possible_actions[position]["closest_human_to_zombie"]=min(
                    possible_actions[position]["closest_human_to_zombie"],
                    closest_human_distance
                )

        # Find more zombies to kill

        killed_zombies_list = [item[1]["zombie_killed"] for item in possible_actions.items()]

        max_zb_kills = max(killed_zombies_list)

        indices = [i for i, x in enumerate(killed_zombies_list) if x == max_zb_kills]

        if len(indices)>1:

            distances = [item[1]["closest_human_to_zombie"] for item in possible_actions.items() if item[1]["zombie_killed"]==max_zb_kills]

            minimum_distance = min(distances)

            indices = list()

            for i, item in enumerate(possible_actions.items()):
                if item[1]["zombie_killed"]==max_zb_kills and item[1]["closest_human_to_zombie"]==minimum_distance:
                    indices.append(i)

            chosen_indice = indices[0]
        else:
            chosen_indice = indices[0]

        position = list(possible_actions.keys())[chosen_indice]

        return Action(position)


    def decide_if_not_humans(self, game_state: Game_State):
        zombies = game_state.by_type()["zombie"]

        allan = game_state._get_allan()


        distances = list()
        for zombie in zombies:
            distances.append(l2_distance_btw_persons(allan, zombie))

        min_dist = min(distances)

        targeted_zombie = zombies[distances.index(min_dist)]

        return Action(targeted_zombie.position)

    def decide(self, game_state: Game_State) -> Action:

        person_map = game_state.by_type()

        if len(person_map["human"])>0:
            return self.decide_if_humans(game_state)
        else:
            return self.decide_if_not_humans(game_state)