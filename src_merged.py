
#----------------------------------------------------------------------------------------------------
# ------------------------- utils/logger.py ------------------------- 

import logging # needed
import sys # needed

logging.basicConfig(stream=sys.stderr, level=logging.INFO)

logger = logging.getLogger("zombies")

#----------------------------------------------------------------------------------------------------
# ------------------------- utils/list.py ------------------------- 
from typing import List # needed

def argmin(value_list: List)->int:
    min_value = min(value_list)
    return value_list.index(min_value)

def argmax(value_list: List)->int:
    max_value = max(value_list)
    return value_list.index(max_value)
#----------------------------------------------------------------------------------------------------
# ------------------------- utils/math.py ------------------------- 
from math import sqrt # needed

def l2_distance(x1: float, y1: float, x2:float, y2:float):
    return sqrt(
        (x2-x1)**2 + (y2-y1)**2
    )
#----------------------------------------------------------------------------------------------------
# ------------------------- utils/optimization/criteria.py ------------------------- 

class Criteria(object):
    """"""

    def __init__(self, field_name: str):
        """Constructor for Criteria"""
        self.field_name = field_name

    def get_field_value(self, data):
        return data[self.field_name]

    def extract_field_value_list(self, data_list: List)->List:

        return list(
            map(
                lambda data: self.get_field_value(data),
                data_list
            )
        )

    def _sort_values(self, values_list: List)->List:
        raise NotImplementedError

    def _get_optimum_value(self, values_list: List):
        raise NotImplementedError

    def filter(self, data_list: List)->List:

        values_list = self.extract_field_value_list(data_list)

        logger.info("Values for field {0}: {1}".format(self.field_name, list(set(values_list))))

        target_value = self._get_optimum_value(values_list)

        return list(
            filter(
                lambda data: self.get_field_value(data)==target_value,
                data_list
                )
        )

    def select(self, data_list: List):
        return self.filter(data_list)[:1]



#----------------------------------------------------------------------------------------------------
# ------------------------- utils/optimization/min_criteria.py ------------------------- 


class Min_Criteria(Criteria):
    """"""

    def sort(self, data_list: List) -> List:
        return sorted(data_list)

    def _get_optimum_value(self, data_list: List):
        return min(data_list)


#----------------------------------------------------------------------------------------------------
# ------------------------- utils/optimization/max_criteria.py ------------------------- 


class Max_Criteria(Criteria):
    """"""

    def sort(self, data_list: List) -> List:
        return sorted(data_list)[::-1]

    def _get_optimum_value(self, data_list: List):
        return max(data_list)


#----------------------------------------------------------------------------------------------------
# ------------------------- utils/optimization/criteria_factory.py ------------------------- 


MAX_CRITERIA_TAG="max"
MIN_CRITERIA_TAG="min"

CRITERIA_MAP=dict({
    MAX_CRITERIA_TAG: Max_Criteria,
    MIN_CRITERIA_TAG: Min_Criteria
})

def criteria_factory(field_name: str, criteria_tag: str):
    global CRITERIA_MAP
    return CRITERIA_MAP[criteria_tag](field_name)

#----------------------------------------------------------------------------------------------------
# ------------------------- utils/optimization/ordered_multi_criteria_optimizer.py ------------------------- 


class Ordered_Multi_Criteria_Optimizer(object):
    """"""

    def __init__(self, criteria_list: List[Criteria]):
        """Constructor for Ordered_Multi_Criteria_Optimizer"""

        self._criteria_list = criteria_list

    def find(self, data_list: List):

        candidates = data_list

        logger.info("Candidates")

        for candidate in candidates:
            logger.info(candidate)

        logger.info("I have {}".format(len(candidates)))

        final_criteria = self._criteria_list[-1]

        criterias = self._criteria_list[:-1]

        for criteria in criterias:

            candidates = criteria.filter(candidates)

            logger.info("Remaining candidates {}".format(len(candidates)))

            if len(candidates)==1:
                break

        if len(candidates) > 1:

            candidates = final_criteria.select(candidates)

        assert len(candidates)==1, "More than one candidate remaining: {}".format(len(candidates))

        return candidates[0]


#----------------------------------------------------------------------------------------------------
# ------------------------- agents/position.py ------------------------- 
class Position(object):

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __repr__(self) -> str:
        return "Position : ({0}, {1})".format(self.x, self.y)
#----------------------------------------------------------------------------------------------------
# ------------------------- agents/person.py ------------------------- 


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

    def __repr__(self) -> str:
        return """

        I am alive

        I am {0} of type {1}

        """.format(self.id, self.type)
#----------------------------------------------------------------------------------------------------
# ------------------------- agents/distance.py ------------------------- 


def _l2_distance_btw_pos(pos1: Position, pos2: Position):
    return l2_distance(pos1.x, pos1.y, pos2.x, pos2.y)

def l2_distance_btw_persons(person1: Person, person2: Person):
    return _l2_distance_btw_pos(person1.position, person2.position)


#----------------------------------------------------------------------------------------------------
# ------------------------- agents/zombie.py ------------------------- 


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
#----------------------------------------------------------------------------------------------------
# ------------------------- agents/human.py ------------------------- 


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
#----------------------------------------------------------------------------------------------------
# ------------------------- agents/action.py ------------------------- 


class Action(object):
    def __init__(self, position: Position):
        self._position = position

    def execute(self):
        print("{0} {1}".format(self._position.x, self._position.y))

    def __repr__(self) -> str:
        return "Action associated with {}".format(self._position)
#----------------------------------------------------------------------------------------------------
# ------------------------- environment/key_figures.py ------------------------- 


HEIGHT = 9000
WIDTH = 16000
#----------------------------------------------------------------------------------------------------
# ------------------------- environment/game_state.py ------------------------- 
from typing import List, Dict # needed



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
                dbt[human][zombie]=l2_distance_btw_persons(human, zombie)

        return dbt

    def log(self):
        for person in self._person_list:
            print(person)
#----------------------------------------------------------------------------------------------------
# ------------------------- environment/zvh_game_state.py ------------------------- 

#----------------------------------------------------------------------------------------------------
# ------------------------- strategies/strategy.py ------------------------- 

class Strategy(object):
    """"""

    def __init__(self):
        """Constructor for Strategy"""
        pass

    def choose_from_env(self, game_state: Game_State)->Action:
        raise NotImplementedError


#----------------------------------------------------------------------------------------------------
# ------------------------- strategies/dumb.py ------------------------- 
import random # needed


class Dumb_Strategy(Strategy):
    """"""

    def choose_from_env(self, game_state: Game_State) -> Action:

        random_position = Position(
            random.randint(0, WIDTH),
            random.randint(0, HEIGHT)
        )

        return Action( position=random_position )

#----------------------------------------------------------------------------------------------------
# ------------------------- strategies/safe.py ------------------------- 

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



#----------------------------------------------------------------------------------------------------
# ------------------------- strategies/zh_strategy.py ------------------------- 

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



#----------------------------------------------------------------------------------------------------
# ------------------------- strategies/closest_zombie_strategy.py ------------------------- 

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



#----------------------------------------------------------------------------------------------------
# ------------------------- strategies/max_zombie_strategy.py ------------------------- 

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



#----------------------------------------------------------------------------------------------------
# ------------------------- strategies/smart_strategy.py ------------------------- 

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



#----------------------------------------------------------------------------------------------------
# ------------------------- agents/allan.py ------------------------- 


class Allan(Human):
    def __init__(self, position: Position):
        super(Allan, self).__init__(position=position, person_id="allan")

        self.velocity = 1000
        self.attack_radius = 2000

    def decide(self, game_state: Game_State)-> Action:
        raise NotImplementedError

    def use_strategy(self, game_state: Game_State, strategy: Strategy)->Action:
        return strategy.choose_from_env(game_state)


#----------------------------------------------------------------------------------------------------
# ------------------------- agents/safe_allan.py ------------------------- 


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
#----------------------------------------------------------------------------------------------------
# ------------------------- agents/a_bit_smarter_allan.py ------------------------- 


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
#----------------------------------------------------------------------------------------------------
# ------------------------- environment/sensor.py ------------------------- 


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
#----------------------------------------------------------------------------------------------------
# ------------------------- main.py ------------------------- 


game_state=None

while True:

    input_dict = input_from_std()

    if game_state is None:
        game_state = start_game_from_dict(input_dict, A_Bit_Smarter_Allan)
    else:
        game_state.update_state(input_dict)

    allan = game_state._get_allan()

    assert isinstance(allan, Allan)

    # action = allan.decide(game_state)

    action = allan.use_strategy(game_state, Smart_Strategy())

    action.execute()
