'''
print(*list(ship_pos_dict.items()), sep='\n')
for ship in battle_state.My:
    print(ship.Id, ship.Position.get_cords())
    pos_l = list(ship.Next_iteration_ship_points.items())
    pprint_pos_list = [pos_l[n: n + 3] for n in range(0, len(pos_l), 3)]
    print(*pprint_pos_list, sep='\n')

print(f"ID: {cur_my_ship.Id} V: {cur_my_ship.Velocity} P: {cur_my_ship.Position} L_P: {last_pos}")

for ship in battle_state.My:
    print(f"ID: {ship.Id} P: {ship.Position} T: {ship.Attack_vector} D: {battle_state.get_distance_ships(ship.Position.get_cords(), ship.Attack_vector.get_cords())}")

for ship in battle_state.My:
    print(ship.Id, ship.Position.get_cords())
    pos_l = list(ship.Next_iteration_ship_points.items())
    pprint_pos_list = [pos_l[n: n + 3] for n in range(0, len(pos_l), 3)]
    print(*pprint_pos_list, sep='\n')

print(f"ID {cur_my_ship.Id} ({cur_my_ship.Position} {Vector(*possible_pos)}) - {nearest_enemy.Position} ({d1}, {d2}) - ({x1}, {x2}) {nearest_enemy_dist}")
'''


def st_pos():
    x = y = z = 12
    xy = zy = zx = (x ** 2 + y ** 2) ** 0.5
    d = xy / 3

    s = (d ** 2 / 2) ** 0.5

    print(f'0: ({0}; {y - s}; {s})',
          f'1: ({s}; {y - s}; {0})',
          f'2: ({x - s}; {s}; {0})',
          f'3: ({x / 2}; {0}; {y / 2})',
          f'4: ({x - s}; {s}; {0})', sep='\n')


def get_pos_block():
    def get_all_blocks_pos(s_cords: tuple, level: int = 0) -> tuple:
        st_p = s_cords[0] - level, s_cords[1] - level, s_cords[2] - level
        row_1 = tuple((st_p[0] + n, st_p[1], st_p[2]) for n in range((level + 1) * 2))
        stk_1 = tuple((p[0], p[1] + n, p[2]) for n in range((level + 1) * 2) for p in row_1)
        res_s = tuple((p[0], p[1], p[2] + n) for n in range((level + 1) * 2) for p in stk_1)
        return res_s
    level = 1
    side = (level + 1) * 2
    field_size = side + 2
    field = [[0] * field_size for _ in range(field_size)]
    zs = []
    for x, y, z in get_all_blocks_pos((0, 0, 0), level):
        zs.append(z)
        field[y + level + 1][x + level + 1] = 1
    print(len(zs), zs)
    print(*field, sep='\n')


# to determine the distance of the attack blaster
def manhattan_distance(point_1: tuple, point_2: tuple) -> int:
    x1, y1, z1, x2, y2, z2 = point_1 + point_2
    return abs(x1 - x2) + abs(y1 - y2) + abs(z1 - z2)


# to determine the distance of the ships
def chebyshev_distance(point_1: tuple, point_2: tuple) -> int:
    x1, y1, z1, x2, y2, z2 = point_1 + point_2
    return max(abs(x1 - x2), abs(y1 - y2), abs(z1 - z2))


# print(manhattan_distance((1, 2, 3), (4, 5, 6)))
# print(chebyshev_distance((1, 2, 3), (4, 5, 6)))

'''field = [[0] * 5 for _ in range(5)]
cords = (1, 1, 1)
st_p = cords[0] - 1, cords[1] - 1, cords[2] - 1
row_1 = tuple((st_p[0] + n, st_p[1], st_p[2]) for n in range(3))
stack_1 = tuple((p[0], p[1] + n, p[2]) for n in range(3) for p in row_1)
cube = tuple((p[0], p[1], p[2] + n) for n in range(3) for p in stack_1)

for p in cube[18:28]:
    field[p[1] + 1][p[0] + 1] = 1
print(*field, sep='\n')'''


# for building rays
def bresenham_3d(point_1: tuple, point_2: tuple, inc_dr_axis: int = 0, max_iter: int = 32) -> list:
    # Python3 code for generating points on a 3-D line
    # using Bresenham's Algorithm
    x1, y1, z1, x2, y2, z2 = point_1 + point_2

    res_points_list, cur_iter = [(x1, y1, z1)], 1
    dx, dy, dz = abs(x2 - x1), abs(y2 - y1), abs(z2 - z1)
    xs = 1 if x2 > x1 else -1
    ys = 1 if y2 > y1 else -1
    zs = 1 if z2 > z1 else -1

    # Driving axis is X-axis"
    if dx >= dy and dx >= dz:
        inc_dr_axis *= xs
        p1 = 2 * dy - dx
        p2 = 2 * dz - dx
        while x1 != (x2 + inc_dr_axis) and cur_iter < max_iter:
            x1 += xs
            if p1 >= 0:
                y1 += ys
                p1 -= 2 * dx
            if p2 >= 0:
                z1 += zs
                p2 -= 2 * dx
            p1 += 2 * dy
            p2 += 2 * dz
            res_points_list.append((x1, y1, z1))
            cur_iter += 1

    # Driving axis is Y-axis"
    elif dy >= dx and dy >= dz:
        inc_dr_axis *= ys
        p1 = 2 * dx - dy
        p2 = 2 * dz - dy
        while y1 != (y2 + inc_dr_axis) and cur_iter < max_iter:
            y1 += ys
            if p1 >= 0:
                x1 += xs
                p1 -= 2 * dy
            if p2 >= 0:
                z1 += zs
                p2 -= 2 * dy
            p1 += 2 * dx
            p2 += 2 * dz
            res_points_list.append((x1, y1, z1))
            cur_iter += 1

    # Driving axis is Z-axis"
    else:
        inc_dr_axis *= zs
        p1 = 2 * dy - dz
        p2 = 2 * dx - dz
        while z1 != (z2 + inc_dr_axis) and cur_iter < max_iter:
            z1 += zs
            if p1 >= 0:
                y1 += ys
                p1 -= 2 * dz
            if p2 >= 0:
                x1 += xs
                p2 -= 2 * dz
            p1 += 2 * dy
            p2 += 2 * dx
            res_points_list.append((x1, y1, z1))
            cur_iter += 1

    return res_points_list


# to determine the distance of the attack blaster
def manhattan_distance(point_1: tuple, point_2: tuple) -> int:
    x1, y1, z1, x2, y2, z2 = point_1 + point_2
    return abs(x1 - x2) + abs(y1 - y2) + abs(z1 - z2)


# to determine the distance of the ships
def chebyshev_distance(point_1: tuple, point_2: tuple) -> int:
    x1, y1, z1, x2, y2, z2 = point_1 + point_2
    return max(abs(x1 - x2), abs(y1 - y2), abs(z1 - z2))


def get_all_blocks_pos(s_cords: tuple, level: int = 0) -> tuple:
    st_p = s_cords[0] - level, s_cords[1] - level, s_cords[2] - level
    row_1 = tuple((st_p[0] + n, st_p[1], st_p[2]) for n in range((level + 1) * 2))
    stk_1 = tuple((p[0], p[1] + n, p[2]) for n in range((level + 1) * 2) for p in row_1)
    res_s = tuple((p[0], p[1], p[2] + n) for n in range((level + 1) * 2) for p in stk_1)
    return res_s


def add_message(m):
    print(m)


def get_distance_ships(ship_1_cords: tuple, ship_2_cords: tuple) -> int:
    ship_1_collision_pos = get_all_blocks_pos(ship_1_cords)
    ship_2_collision_pos = get_all_blocks_pos(ship_2_cords)
    closest_ship_1_point = min(
        [(point, chebyshev_distance(point, ship_2_cords))
         for point in ship_1_collision_pos], key=lambda p: p[1])[0]
    res_chebyshev_distance = min(
        [chebyshev_distance(point, closest_ship_1_point)
         for point in ship_2_collision_pos]) - 1

    return res_chebyshev_distance


def get_coordinate_line(ship_1_cords, ship_2_cords, inc_dr_axis=0, max_iter=32) -> list:
    ship_1_collision_pos = get_all_blocks_pos(ship_1_cords)
    ship_2_collision_pos = get_all_blocks_pos(ship_2_cords)
    closest_ship_1_point = min(
        [(point, chebyshev_distance(point, ship_2_cords))
         for point in ship_1_collision_pos], key=lambda p: p[1])[0]
    closest_ship_2_point = min(
        [(point, chebyshev_distance(point, closest_ship_1_point))
         for point in ship_2_collision_pos], key=lambda p: p[1])[0]
    cords_list = bresenham_3d(
        closest_ship_1_point, closest_ship_2_point,
        inc_dr_axis, max_iter)

    return cords_list


# print(f"{(11, 11, 11), (17, 17, 17)}: {get_coordinate_line((11, 11, 11), (17, 17, 17))}")
# print(get_distance_ships((11, 11, 11), (17, 17, 17)))
move_selection_weights_dict = {
    'background_weight_coefficient': 2,
    'to_center_weight_coefficient': 5,
    'enemy_con_weight_coefficient': 2,
    'allies_focused_weight_coefficient': 2,
    'enemy_distance_weights': {
        "small": -1,
        "medium": 3,
        "large": 2,
        "neutral": 1
    },
    'allies_distance_weight': 2,
    'friendly_fire__weights': {
        'friendly_fire_true': 1,
        'f_f_enemy_focused': 1,
        'ally_ship_targets': 1
    }
}


def get_interacting_blocks(ship_1_cords, ship_2_cords) -> tuple:
    ship_1_collision_pos = get_all_blocks_pos(ship_1_cords)
    ship_2_collision_pos = get_all_blocks_pos(ship_2_cords)
    closest_ship_1_point = min(
        [(point, chebyshev_distance(point, ship_2_cords))
         for point in ship_1_collision_pos], key=lambda p: p[1])[0]
    closest_ship_2_point = min(
        [(point, chebyshev_distance(point, closest_ship_1_point))
         for point in ship_2_collision_pos], key=lambda p: p[1])[0]
    return closest_ship_1_point, closest_ship_2_point


def get_coordinate_line(ship_1_cords, ship_2_cords, inc_dr_axis=0, max_iter=32) -> list:
    closest_ship_1_point, closest_ship_2_point = \
        get_interacting_blocks(ship_1_cords, ship_2_cords)
    cords_list = bresenham_3d(
        closest_ship_1_point, closest_ship_2_point,
        inc_dr_axis, max_iter)
    return cords_list


blaster_ray_cords = tuple(get_coordinate_line(
        *get_interacting_blocks((0, 0, 0), (4, 3, 5)), inc_dr_axis=6)[1:6])
print(blaster_ray_cords)
