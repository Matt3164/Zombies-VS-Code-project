from pyzombies.environment.sensor import start_game_from_dict, input_from_std
from pyzombies.agents.a_bit_smarter_allan import A_Bit_Smarter_Allan
from pyzombies.agents.allan import Allan
from pyzombies.strategies.dumb import Dumb_Strategy
from pyzombies.strategies.safe import Safe_Strategy
from pyzombies.strategies.max_zombie_strategy import Max_Zombie_Strategy
from pyzombies.strategies.smart_strategy import Smart_Strategy


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
