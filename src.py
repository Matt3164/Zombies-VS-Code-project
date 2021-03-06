from main import game_state, input_dict
from pyzombies.agents.a_bit_smarter_allan import A_Bit_Smarter_Allan
from pyzombies.agents.allan import Allan
from pyzombies.environment.sensor import input_from_std, start_game_from_dict

game_state = None

while True:

    if game_state is None:
        game_state = start_game_from_dict(input_dict, A_Bit_Smarter_Allan)
    else:
        game_state.update_state(input_dict)

    allan = game_state._get_allan()

    assert isinstance(allan, Allan)

    action = allan.decide(game_state)

    action.execute()




















