from typing import List, Dict # needed

from pyzombies.agents.human import Human
from pyzombies.agents.person import Person
from pyzombies.agents.position import Position
from pyzombies.agents.zombie import Zombie
from pyzombies.agents.distance import l2_distance_btw_persons


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