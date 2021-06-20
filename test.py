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

    # for ship in battle_state.My:
    #     print(ship.Id, ship.Position.get_cords())
    #     pos_l = list(ship.Next_iteration_ship_points.items())
    #     pprint_pos_list = [pos_l[n: n + 3] for n in range(0, len(pos_l), 3)]
    #     print(*pprint_pos_list, sep='\n')
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

from numpy import nanmean


print(sum(map(lambda e: e, [1, 2, 3])))

