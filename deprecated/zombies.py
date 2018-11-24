from typing import List, Dict, Tuple
import sys


DO_LOG=False

def logger(msg):
    global DO_LOG
    if DO_LOG:
        print(msg, file=sys.stderr)


def input_from_std():
    x, y = [int(i) for i in input().split()]

    human_count = int(input())

    human_list = list()

    for i in range(human_count):
        human_id, human_x, human_y = [int(j) for j in input().split()]

        human_list.append(
            dict(id=human_id, x=human_x, y=human_y)
        )

    zombie_count = int(input())

    zombie_list = list()
    for i in range(zombie_count):
        zombie_id, zombie_x, zombie_y, zombie_xnext, zombie_ynext = [int(j) for j in input().split()]

        zombie_list.append(
            dict(id=zombie_id, x=zombie_x, y=zombie_y, x_next=zombie_xnext, y_next=zombie_ynext)
        )

    return dict(
        player=dict(x=x, y=y),
        humans=human_list,
        zombies=zombie_list
    )


class Position(object):

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __repr__(self) -> str:
        return "Position : ({0}, {1})".format(self.x, self.y)


from math import sqrt

def l2_distance(pos1: Position, pos2: Position):

    logger("Computing dist between {0} and {1}".format(pos1, pos2))

    dist = sqrt(
        (float(pos2.x)-float(pos1.x))**2 + (float(pos2.y)-float(pos1.y))**2
    )

    logger("Dist: {}".format(dist))

    return dist

class Person(object):

    def __init__(self,
                 person_id: str,
                 position: Position
                 ):
        self.position = position
        self.id = person_id

        self.velocity = None
        self.attack_radius = None

        self.is_alive = True

        self.type = None

    def move(self, game_state):
        raise NotImplementedError

    def die(self):
        self.is_alive=False

    def distance_to(self, person):
        return l2_distance(self.position, person.position)

    def __repr__(self) -> str:
        return """

        I am alive

        I am {0} of type {1}

        """.format(self.id, self.type)


class Human(Person):

    def __init__(self,
                 person_id: str,
                 position: Position
                 ):
        super(Human, self).__init__(person_id, position)

        self.type = "human"

        self.velocity = 0.
        self.attack_radius = 0.

        self.is_alive = True


class Zombie(Person):

    def __init__(self,
                 person_id: str,
                 position: Position
                 ):
        super(Zombie, self).__init__(person_id, position)

        self.type = "zombie"

        self.velocity = 400.
        self.attack_radius = 400.

        self.is_alive = True

    def move(self, game_state):
        self.position = self._next_position
        self._next_position = None

class Game_State(object):
    def __init__(self,
                 person_list: List[Person],
                 t: int=0,
                 ):
        self._person_list = person_list

        self.t = t

        self.height = 9000
        self.width = 16000

        self.dead_persons = list()

    def get_by_id(self, exid):
        return list(filter(lambda person: person.id==exid, self._person_list))[0]

    def _get_allan(self):
        return self.get_by_id("allan")

    def get_current_state(self, input_dict):
        allan = self._get_allan()

        allan.position = Position(input_dict["player"]["x"], input_dict["player"]["y"])

        persons = list()

        for human_dict in input_dict['humans']:
            position = Position(
                human_dict["x"],
                human_dict["y"]
            )
            persons.append(
                Human(position=position, person_id=human_dict["id"])
            )

        for zombie_dict in input_dict['zombies']:

            position = Position(
                zombie_dict["x_next"],
                zombie_dict["y_next"]
            )
            persons.append(
                Zombie(
                    position=position,
                    person_id=zombie_dict["id"],
                )
            )

        return persons + [allan]

    def update_state(self, input_dict):

        new_list_of_persons = self.get_current_state(input_dict)

        # Compute list of dead persons : currently, list of ids, next steps list of persons

        old_ids = [ person.id for person in self._person_list]

        new_ids = [person.id for person in new_list_of_persons]

        dead_ids = list(set(old_ids) - set(new_ids))

        self.dead_persons += dead_ids

        self._person_list = new_list_of_persons

        self.t+=1

    def graveyard(self)->List[str]:
        return self.dead_persons

    def get_types(self)->List[str]:
        return list(set([person.type for person in self._person_list]))

    def by_type(self)->Dict[str, List[Person]]:

        by_type_map=dict()

        for person in self._person_list:
            if not ( person.type in by_type_map.keys() ):
                by_type_map[person.type]=list()

            by_type_map[person.type].append(person)

        return by_type_map

    def distance_between_types(self)->Dict[Person, Dict[Person, float]]:

        dbt = dict()

        type_map = self.by_type()

        for human in type_map["human"]:
            dbt[human]=dict()
            for zombie in type_map["zombie"]:
                dbt[human][zombie]=human.distance_to(zombie)

        return dbt

    def log(self):
        for person in self._person_list:
            print(person)


class Action(object):
    def __init__(self, position: Position):
        self._position = position

    def execute(self):
        print("{0} {1}".format(self._position.x, self._position.y))

    def __repr__(self) -> str:
        return "Action associated with {}".format(self._position)


class Allan(Human):
    def __init__(self, position: Position):
        super(Allan, self).__init__(position=position, person_id="allan")

        self.velocity = 1000
        self.attack_radius = 2000

    def decide(self, game_state: Game_State)->Action:
        raise NotImplementedError

class Safe_Allan(Allan):

    def decide(self, game_state: Game_State)->Action:

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

class A_Bit_Smarter_Allan(Allan):

    def decide_if_humans(self, game_state: Game_State):

        zombies = game_state.by_type()["zombie"]

        humans = game_state.by_type()["human"]

        possible_actions = dict()

        for zombie in zombies:

            position = zombie.position

            new_action = Action(zombie.position)

            closest_human_distance = min([ zombie.distance_to(human) for human in humans ])

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

        logger("Possible kills {}".format(list(set(killed_zombies_list))))

        max_zb_kills = max(killed_zombies_list)

        indices = [i for i, x in enumerate(killed_zombies_list) if x == max_zb_kills]

        if len(indices)>1:

            distances = [item[1]["closest_human_to_zombie"] for item in possible_actions.items() if item[1]["zombie_killed"]==max_zb_kills]

            minimum_distance = min(distances)

            logger("Distances to human {0} and minimum {1}".format(distances, minimum_distance))

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
            distances.append(allan.distance_to(zombie))

        min_dist = min(distances)

        targeted_zombie = zombies[distances.index(min_dist)]

        return Action(targeted_zombie.position)

    def decide(self, game_state: Game_State) -> Action:

        person_map = game_state.by_type()

        if len(person_map["human"])>0:
            return self.decide_if_humans(game_state)
        else:
            return self.decide_if_not_humans(game_state)


def start_game_from_dict(input_dict, allan_class=Allan):
    allan_position = Position(input_dict["player"]["x"], input_dict["player"]["y"])

    allan = allan_class(allan_position)

    persons = list()

    for human_dict in input_dict['humans']:
        position = Position(
            human_dict["x"],
            human_dict["y"]
        )
        persons.append(
            Human(position=position, person_id=human_dict["id"])
        )

    for zombie_dict in input_dict['zombies']:
        position = Position(
            zombie_dict["x_next"],
            zombie_dict["y_next"]
        )
        persons.append(
            Zombie(
                position=position,
                person_id=zombie_dict["id"],
            )
        )

    return Game_State(persons + [allan])

# if __name__ == '__main__':
#
#     input_dict = dict(
#         player = dict(x=1000, y=1000),
#         humans = [ dict(id="toto", x=100, y=100),  dict(id="tata", x=100, y=1900)],
#         zombies = [
#             dict(id="zomb", x=1500, y=1000, x_next=1250, y_next=1000)
#     ]
#     )
#
#     game_state = start_game_from_dict(input_dict, A_Bit_Smarter_Allan)
#
#     print("T={}".format(game_state.t))
#     game_state.log()
#
#     input_dict = dict(
#         player=dict(x=1000, y=1000),
#         humans=[],
#         zombies=[
#             dict(id="zomb", x=1500, y=1000, x_next=1250, y_next=1000)
#         ]
#     )
#
#     game_state.update_state(input_dict)
#     print("T={}".format(game_state.t))
#     game_state.log()
#
#     allan = game_state._get_allan()
#
#     assert isinstance(allan, Allan)
#
#     action = allan.decide(game_state)
#
#     action.execute()

game_state=None
while True:

    input_dict = input_from_std()

    if game_state is None:
        game_state = start_game_from_dict(input_dict, A_Bit_Smarter_Allan)
    else:
        game_state.update_state(input_dict)

    allan = game_state._get_allan()

    assert isinstance(allan, Allan)

    action = allan.decide(game_state)

    action.execute()




















