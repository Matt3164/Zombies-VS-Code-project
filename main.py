game_state=None
input_dict = input_from_std()

while True:

    if game_state is None:
        game_state = start_game_from_dict(input_dict, A_Bit_Smarter_Allan)
    else:
        game_state.update_state(input_dict)

    allan = game_state._get_allan()

    assert isinstance(allan, Allan)

    action = allan.decide(game_state)

    action.execute()
