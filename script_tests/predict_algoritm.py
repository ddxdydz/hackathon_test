'''
# Motion predictions for weak and frequent algorithms
predict_enemy_pos = {}
for e_ship in opponent:
    # To verify the assumption predict
    cur_enemy_pos = e_ship.Position.get_cords()
    cur_enemy_vil = e_ship.Velocity.get_cords()
    last_enemy_pos = \
        cur_enemy_pos[0] - cur_enemy_vil[0], \
        cur_enemy_pos[1] - cur_enemy_vil[1], \
        cur_enemy_pos[1] - cur_enemy_vil[1]
    predict_enemy_target = min(data["My"], key=lambda f_ship: cls.get_distance_ships(
        e_ship.Position.get_cords(), f_ship.Position.get_cords()))
    predict_enemy_move = bresenham_3d(
        e_ship.Position.get_cords(),
        predict_enemy_target.Position.get_cords(),
        max_iter=2)[-1]
'''