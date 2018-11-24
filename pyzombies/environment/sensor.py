from pyzombies.agents.allan import Allan
from pyzombies.agents.human import Human
from pyzombies.agents.position import Position
from pyzombies.agents.zombie import Zombie
from pyzombies.environment.game_state import Game_State


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