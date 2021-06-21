start_position_ship = {
    0: (0, 3, 3),
    1: (0, 0, 5),
    2: (3, 0, 3),
    3: (3, 3, 0),
    4: (5, 0, 0)
}
is_on_start_position = False
check_reverse = False


'''# Realization of movement to a given starting position:
if not is_on_start_position:
    # Check Reverse
    if not check_reverse:
        if battle_state.My[0].Position.get_cords()[0] > 15:
            start_position_ship = \
                {key: tuple(30 - value[n] - 2 for n in range(len(value)))
                 for key, value in start_position_ship.items()}
        check_reverse = True
    # Checking occupied positions
    if all(map(lambda n_ship:
               battle_state.My[n_ship].Position.get_cords() == start_position_ship[n_ship],
               range(len(battle_state.My)))):
        is_on_start_position = True
    else:
        # Move detection
        for num_ship, cur_my_ship in enumerate(battle_state.My):
            do_move = True
            cur_my_ship.add_correct_move(Vector(*start_position_ship[num_ship]))
            # Check the allies distance to prevent a collision
            cur_friendly_ship_cords = \
                battle_state.get_all_blocks_pos(cur_my_ship.Move_vector.get_cords())
            for friendly_ship in battle_state.My:
                if friendly_ship.Id != cur_my_ship.Id:
                    sum_a_cords = battle_state.Ships_collision_pos[friendly_ship.Id] + \
                                  cur_friendly_ship_cords
                    if len(set(sum_a_cords)) != len(sum_a_cords):
                        do_move = False
                        break
            if do_move:
                # Updating the battle_state.Ships_collision_pos
                battle_state.Ships_collision_pos[cur_my_ship.Id] = \
                    battle_state.get_all_blocks_pos(
                        cur_my_ship.Move_vector.get_cords())

                battle_output.UserCommands.append(
                    UserCommand(Command="MOVE", Parameters=MoveCommandParameters(
                        cur_my_ship.Id, cur_my_ship.Move_vector)))
        battle_output.Message = f"To starting position..."
        messages.clear()
        return battle_output'''
