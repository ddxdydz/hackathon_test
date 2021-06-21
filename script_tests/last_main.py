import json

ALLIES_DISTANCE = 0
BORDERLINE_SUICIDE_ATTACK = 30


def get_cords(some_ship: dict) -> tuple:
    cords = tuple(map(int, some_ship["Position"].split('/')))
    return cords


def get_distance(ship_1, ship_2):
    cords_1 = get_cords(ship_1)
    cords_2 = get_cords(ship_2)
    return ((cords_1[0] - cords_2[0]) ** 2 +
            (cords_1[1] - cords_2[1]) ** 2 +
            (cords_1[2] - cords_2[2]) ** 2) ** 0.5


def get_depart_cords(ship_1, ship_2):
    cords_1 = get_cords(ship_1)
    cords_2 = get_cords(ship_2)
    values_list = [
        cords_2[cords_num] - cords_1[cords_num]
        for cords_num in range(0, 3)
    ]
    max_elem = max(values_list) if max(values_list) else 1
    move_target = presented_cords(tuple(
        round(cords_1[cords_num] - values_list[cords_num] / max_elem)
        for cords_num in range(0, 3)
    ))
    return move_target


def check_borders(cords: tuple) -> tuple:
    res_cords = tuple(map(
        lambda cord: 28 if cord > 28 else 1 if cord < 1 else cord,
        cords)
    )
    return res_cords


def presented_cords(cords: tuple) -> str:
    new_cords = check_borders(cords)
    return f"{new_cords[0]}/{new_cords[1]}/{new_cords[2]}"


def make_draft(data: dict) -> dict:
    draft = {}
    # TODO: Make draft here
    return draft


def make_turn(data: dict) -> dict:
    battle_output = {
        'Message': f"I have {len(data['My'])} ships and move to center of galaxy and shoot",
        'UserCommands': []
    }

    for friendly_ship in data["My"]:
        target_enemy = min(
            data["Opponent"],
            key=lambda enemy_ship: get_distance(
                friendly_ship,
                enemy_ship
            )
        )
        other_allies = list(filter(
            lambda ship: ship["Id"] != friendly_ship["Id"],
            data["My"]
        ))
        closest_ally = min(
            other_allies,
            key=lambda allies_ship: get_distance(friendly_ship, allies_ship)
        ) if other_allies else []

        move_target = '15/15/15'
        gun_target = target_enemy["Position"]

        if friendly_ship["Health"] < BORDERLINE_SUICIDE_ATTACK:
            move_target = target_enemy["Position"]
        elif not other_allies or get_distance(closest_ally, friendly_ship) >= ALLIES_DISTANCE:
            target_distance = get_distance(friendly_ship, target_enemy)
            if 4 < target_distance <= 5:
                move_target = friendly_ship["Position"]
            elif target_distance > 5:
                move_target = target_enemy["Position"]
            elif target_distance < 4:
                move_target = get_depart_cords(target_enemy, friendly_ship)
        else:
            move_target = get_depart_cords(closest_ally, friendly_ship)

        battle_output['UserCommands'].append({
            "Command": "MOVE",
            "Parameters": {
                'Id': friendly_ship['Id'],
                'Target': move_target
            }
        })

        guns = [x for x in friendly_ship['Equipment'] if x['Type'] == 1]
        if guns:
            gun = guns[0]
            battle_output['UserCommands'].append({
                "Command": "ATTACK",
                "Parameters": {
                    'Id': friendly_ship['Id'],
                    'Name': gun['Name'],
                    'Target': gun_target
                }
            })

    return battle_output


def play_game():
    while True:
        raw_line = input()
        line = json.loads(raw_line)
        if 'PlayerId' in line:
            print(json.dumps(make_draft(line), ensure_ascii=False))
        elif 'My' in line:
            print(json.dumps(make_turn(line), ensure_ascii=False))


if __name__ == '__main__':
    play_game()
