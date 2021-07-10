import json
from datetime import datetime

from player_1 import play_game_step as player_1_step
from player_2 import play_game_step as player_2_step

BLOCK_PLAYER_1_ID = 12341
BLOCK_PLAYER_2_ID = 41415
BLOCK_RAY_PLAYER_1_ID = 52646
BLOCK_RAY_PLAYER_2_ID = 96646
BLOCK_END_BLASTER_RAY_ID = 64212
BLOCK_TAKE_DAMAGE_ID = 53268

STEP_LIMIT = 1000
DRAW = 'It\'s a draw game'
P1_WON = 'Player1 won!'
P2_WON = 'Player2 won!'
messages = []
battle = {}


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


# for debugging process
def add_message(message: str):
    global messages
    messages.append(message)


def tuple_format_cords(cords: str) -> tuple:
    return tuple(map(int, cords.split('/')))


def str_format_cords(cords: tuple) -> str:
    return f"{cords[0]}/{cords[1]}/{cords[2]}"


def get_all_blocks_pos(s_cords: tuple, level: int = 0) -> tuple:
    st_p = s_cords[0] - level, s_cords[1] - level, s_cords[2] - level
    row_1 = tuple((st_p[0] + n, st_p[1], st_p[2]) for n in range((level + 1) * 2))
    stk_1 = tuple((p[0], p[1] + n, p[2]) for n in range((level + 1) * 2) for p in row_1)
    res_s = tuple((p[0], p[1], p[2] + n) for n in range((level + 1) * 2) for p in stk_1)
    return res_s


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


def get_coordinate_line(ship1_pos, ship2_pos, inc_dr_axis=0, max_iter=32) -> list:
    cords_list = bresenham_3d(
        ship1_pos, ship2_pos,
        inc_dr_axis, max_iter)
    return cords_list


def get_correct_move(cur_pos: tuple, target: tuple):
    return bresenham_3d(cur_pos, target, max_iter=2)[-1]


def get_blaster_ray(cur_pos: tuple, target: tuple):
    ship_collision_pos = get_all_blocks_pos(cur_pos)
    closest_ship_point = min(
        [(point, chebyshev_distance(point, target))
         for point in ship_collision_pos], key=lambda p: p[1])[0]
    blaster_ray_cords = tuple(get_coordinate_line(closest_ship_point, target, inc_dr_axis=6)[1:6])
    return blaster_ray_cords


def check_borders(cords: tuple) -> bool:
    return all(map(lambda cord: 0 <= cord <= 28, cords))


with open(r'init_json\BattleState_p1.json', 'r', encoding='utf8') as file:
    data = file.read()
    battle_state_p1 = \
        json.loads(data)
with open(r'init_json\BattleState_p2.json', 'r', encoding='utf8') as file:
    data = file.read()
    battle_state_p2 = \
        json.loads(data)

step_num = 0
while True:
    step_num += 1

    player_1_blaster_rays = []
    player_2_blaster_rays = []
    blaster_damage_blocks = []
    player_1_pos = []
    player_2_pos = []

    object_positions = []
    output_message = ''

    output_message += f'\nStep: {step_num}'

    battle_output_p1 = player_1_step(battle_state_p1)
    battle_output_p2 = player_2_step(battle_state_p2)

    p1_ship_ids = list(map(lambda s: s["Id"], battle_state_p1["My"]))
    p2_ship_ids = list(map(lambda s: s["Id"], battle_state_p2["My"]))

    ships = \
        {ship["Id"]: {
            "Velocity": tuple_format_cords(ship["Velocity"]),
            "Position": tuple_format_cords(ship["Position"]),
            "Next_position": tuple_format_cords(ship["Position"]),
            "Health": ship["Health"],
            "PlayerID": 1 if ship["Id"] in p1_ship_ids else 2}
            for ship in battle_state_p1["My"] + battle_state_p2["My"]}

    commands = battle_output_p1['UserCommands'] + battle_output_p2['UserCommands']
    for command in commands:
        if command['Command'] != 'ATTACK':
            command['Parameters']['Target'] = \
                get_correct_move(
                    ships[command['Parameters']['Id']]["Position"],
                    tuple_format_cords(command['Parameters']['Target'])
                )
        else:
            command['Parameters']['Target'] = \
                tuple_format_cords(command['Parameters']['Target'])
    move_commands = list(filter(lambda cm: cm['Command'] in ('MOVE', 'ACCELERATE'), commands))
    attack_commands = list(filter(lambda cm: cm['Command'] == 'ATTACK', commands))

    # Check ram attack
    were_changes = True
    while were_changes:
        were_changes = False
        for move_command in move_commands:
            ship_command_id = move_command['Parameters']['Id']
            if ships[ship_command_id]["Next_position"] != \
                    move_command['Parameters']['Target']:
                ship_cols = []
                for s_id in ships.keys():
                    if s_id != ship_command_id:
                        ship_cols += list(get_all_blocks_pos(ships[s_id]["Next_position"]))
                sum_a_cords = tuple(set(ship_cols)) + get_all_blocks_pos(
                    move_command["Parameters"]["Target"])
                if len(set(sum_a_cords)) == len(sum_a_cords):
                    output_message += f'\nMOVE: ID:{ship_command_id} from {ships[ship_command_id]["Next_position"]} ' +\
                                      f'to {move_command["Parameters"]["Target"]}'
                    ships[ship_command_id]["Next_position"] = \
                        move_command["Parameters"]["Target"]
                    were_changes = True
    for move_command in move_commands:
        ship_command_id = move_command['Parameters']['Id']
        if ships[ship_command_id]["Next_position"] != move_command['Parameters']['Target']:
            cur_ship_next_col = get_all_blocks_pos(move_command['Parameters']['Target'])
            for s_id in ships.keys():
                if s_id != ship_command_id:
                    sum_a_cords = get_all_blocks_pos(
                        ships[s_id]["Next_position"]) + cur_ship_next_col
                    if len(set(sum_a_cords)) != len(sum_a_cords):
                        output_message += f'\nRAM ATTACK: ID:{ship_command_id} ram attack to ID:{s_id}'
                        ships[ship_command_id]["Health"] -= 2
                        ships[s_id]["Health"] -= 2
                        # Check vector
                        next_x, next_y, next_z = ships[s_id]['Next_position']
                        ram_xv, ram_yv, ram_zv = (
                            ships[ship_command_id]["Next_position"][n] - move_command['Parameters']['Target'][n]
                            for n in range(3)
                        )
                        cords = next_x + ram_xv, next_y + ram_yv, next_z + ram_zv
                        ship_cols = []
                        for i in ships.keys():
                            if i != s_id:
                                ship_cols += list(get_all_blocks_pos(ships[i]["Next_position"]))
                        sum_a_cords = get_all_blocks_pos(cords) + tuple(set(ship_cols))
                        if len(set(sum_a_cords)) != len(sum_a_cords):
                            output_message += f'\nRAM IMPULS: {ship_command_id} -> {s_id} from {ships[s_id]["Next_position"]} to {cords} - VEL {ram_xv, ram_yv, ram_zv} - N {ships[ship_command_id]["Next_position"]} - T {move_command["Parameters"]["Target"]}'
                            ships[s_id]["Next_position"] = cords

    # Check borders
    for s_id in ships.keys():
        if not check_borders(ships[s_id]["Next_position"]):
            ships[s_id]["Health"] -= ships[s_id]["Health"] ** 2
            output_message += f'\nBORDER: ID:{s_id} from borders'

    for ship_id in ships.keys():
        append_list = player_1_pos if ships[ship_id]["PlayerID"] == 1 else player_2_pos
        append_list += list(get_all_blocks_pos(ships[ship_id]["Next_position"]))
    res_player_1_pos = [(BLOCK_PLAYER_1_ID, pos) for pos in player_1_pos]
    res_player_2_pos = [(BLOCK_PLAYER_2_ID, pos) for pos in player_2_pos]
    battle[step_num] = {
        'step': step_num,
        'object_positions': res_player_1_pos + res_player_2_pos,
        'message': output_message,
        'player_1_info': battle_state_p1["My"],
        'player_2_info': battle_state_p1["Opponent"]
    }

    # Check blaster damage
    for attack_command in attack_commands:
        ship_command_id = attack_command['Parameters']['Id']
        ship_pos = ships[ship_command_id]["Next_position"]
        ship_target = attack_command['Parameters']['Target']

        blaster_ray = get_blaster_ray(ship_pos, ship_target)
        if ships[ship_command_id]["PlayerID"] == 1:
            player_1_blaster_rays.append(blaster_ray)
        elif ships[ship_command_id]["PlayerID"] == 2:
            player_2_blaster_rays.append(blaster_ray)
        for s_id in ships.keys():
            if ship_command_id != s_id:
                cur_ship_next_col = get_all_blocks_pos(ships[s_id]["Next_position"])
                sum_a_cords = cur_ship_next_col + blaster_ray
                if len(set(sum_a_cords)) != len(sum_a_cords):
                    for elem in set(cur_ship_next_col) & set(blaster_ray):
                        blaster_damage_blocks.append(elem)
                    output_message += f'\nSHOOT ATTACK: ID:{ship_command_id} shoot attack to ID:{s_id}'
                    ships[s_id]["Health"] -= 5

    battle_state_p1 = {
        "My": [
            {
                "Id": s_id,
                "Velocity": str_format_cords(tuple(
                    ships[s_id]["Next_position"][i] - ships[s_id]["Position"][i] for i in range(3))),
                "Position": str_format_cords(ships[s_id]["Next_position"]),
                "Health": ships[s_id]["Health"]
            } for s_id in ships if ships[s_id]['PlayerID'] == 1 and ships[s_id]["Health"] > 0
        ],
        "Opponent": [
            {
                "Id": s_id,
                "Velocity": str_format_cords(tuple(
                    ships[s_id]["Next_position"][i] - ships[s_id]["Position"][i] for i in range(3))),
                "Position": str_format_cords(ships[s_id]["Next_position"]),
                "Health": ships[s_id]["Health"]
            } for s_id in ships if ships[s_id]['PlayerID'] == 2 and ships[s_id]["Health"] > 0
        ],
        "FireInfos": [{}]
    }
    battle_state_p2["My"], battle_state_p2["Opponent"] = \
        battle_state_p1["Opponent"], battle_state_p1["My"]

    count_p1_ships = len(battle_state_p1["My"])
    count_p2_ships = len(battle_state_p2["My"])

    output_message += '\n' + 'Player1 ships:'
    for ship in battle_state_p1['My']:
        output_message += \
            '\n' + f"Id: {ship['Id']}, Health: {ship['Health']}, " \
                   f"Position: {ship['Position']}, Velocity: {ship['Velocity']}"
    output_message += '\n' + 'Player2 ships:'
    for ship in battle_state_p2['My']:
        output_message += \
            '\n' + f"Id: {ship['Id']}, Health: {ship['Health']}, " \
                   f"Position: {ship['Position']}, Velocity: {ship['Velocity']}"
    output_message += '\n'

    end_blaster_ray = [ray[-1] for ray in player_1_blaster_rays] + [ray[-1] for ray in player_2_blaster_rays]
    res_player_1_blaster_rays = []
    for rays in player_1_blaster_rays:
        res_player_1_blaster_rays += list(set(rays) - set(blaster_damage_blocks + end_blaster_ray))
    res_player_2_blaster_rays = []
    for rays in player_2_blaster_rays:
        res_player_2_blaster_rays += list(set(rays) - set(blaster_damage_blocks + end_blaster_ray))
    res_end_blaster_rays = list(set(end_blaster_ray) - set(blaster_damage_blocks))
    res_player_1_pos = list(set(player_1_pos) - set(blaster_damage_blocks))
    res_player_2_pos = list(set(player_2_pos) - set(blaster_damage_blocks))
    res_blaster_damage_blocks = blaster_damage_blocks

    res_player_1_pos = [(BLOCK_PLAYER_1_ID, pos) for pos in res_player_1_pos]
    res_player_2_pos = [(BLOCK_PLAYER_2_ID, pos) for pos in res_player_2_pos]
    res_player_1_blaster_rays = [(BLOCK_RAY_PLAYER_1_ID, ray) for ray in res_player_1_blaster_rays]
    res_player_2_blaster_rays = [(BLOCK_RAY_PLAYER_2_ID, ray) for ray in res_player_2_blaster_rays]
    res_end_blaster_rays = [(BLOCK_END_BLASTER_RAY_ID, pos) for pos in res_end_blaster_rays]
    res_blaster_damage_blocks = [(BLOCK_TAKE_DAMAGE_ID, pos) for pos in res_blaster_damage_blocks]

    object_positions.extend(set(
        res_player_1_pos +
        res_player_2_pos +
        res_player_1_blaster_rays +
        res_player_2_blaster_rays +
        res_end_blaster_rays +
        res_blaster_damage_blocks
    ))

    step_num += 1
    battle[step_num] = {
        'step': step_num,
        'object_positions': object_positions,
        'message': output_message,
        'player_1_info': battle_state_p1["My"],
        'player_2_info': battle_state_p1["Opponent"]
    }

    print(output_message)

    res = 'dw'
    if not count_p1_ships and count_p2_ships:
        res = 'p2'
        output_message += '\n' + P2_WON
        break
    elif count_p1_ships and not count_p2_ships:
        res = 'p1'
        output_message += '\n' + P1_WON
        break
    if step_num > STEP_LIMIT or not (count_p1_ships or count_p2_ships):
        output_message += '\n' + DRAW
        break

now = ''.join([elem for elem in str(datetime.now()) if elem.isdigit()])
filename = f'battles/battle_{now}_{res}.json'
with open(filename, 'w', encoding='utf8') as file:
    json.dump(battle, file, ensure_ascii=True, sort_keys=True)
