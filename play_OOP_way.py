import json
from dataclasses import dataclass
from enum import Enum
from typing import List, Optional

messages = []


class JSONCapability:
    def to_json(self):
        return {
            k: v if not isinstance(v, Vector) else str(v)
            for k, v in self.__dict__.items()
            if v is not None
        }


# region primitives
@dataclass
class Vector:
    X: int
    Y: int
    Z: int

    @classmethod
    def from_json(cls, data):
        x, y, z = map(int, data.split('/'))
        return cls(x, y, z)

    def get_cords(self) -> tuple:
        return self.X, self.Y, self.Z

    def __str__(self):
        return f"{self.X}/{self.Y}/{self.Z}"


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


# endregion

# region battle commands

@dataclass
class CommandParameters(JSONCapability):
    pass


@dataclass
class AttackCommandParameters(CommandParameters):
    Id: int
    Name: str
    Target: Vector


@dataclass
class MoveCommandParameters(CommandParameters):
    Id: int
    Target: Vector


@dataclass
class AccelerateCommandParameters(CommandParameters):
    Id: int
    Vector: Vector


@dataclass
class UserCommand(JSONCapability):
    Command: str
    Parameters: CommandParameters


@dataclass
class BattleOutput(JSONCapability):
    Message: str = None
    UserCommands: List[UserCommand] = None


# endregion

# region draft commands
@dataclass
class DraftChoice(JSONCapability):
    # TODO Make draft choice
    pass


@dataclass
class DraftOptions:
    # TODO: Parse draft options
    pass


# endregion

# region equipment

class EquipmentType(Enum):
    Energy = 0
    Gun = 1
    Engine = 2
    Health = 3


class EffectType(Enum):
    Blaster = 0


@dataclass
class EquipmentBlock(JSONCapability):
    Name: str
    Type: EquipmentType

    @classmethod
    def from_json(cls, data):
        if EquipmentType(data['Type']) == EquipmentType.Energy:
            return EnergyBlock(**data)
        elif EquipmentType(data['Type']) == EquipmentType.Gun:
            return GunBlock(**data)
        elif EquipmentType(data['Type']) == EquipmentType.Engine:
            return EngineBlock(**data)
        elif EquipmentType(data['Type']) == EquipmentType.Health:
            return HealthBlock(**data)


@dataclass
class EnergyBlock(EquipmentBlock):
    IncrementPerTurn: int
    MaxEnergy: int
    StartEnergy: int
    Type = EquipmentType.Energy


@dataclass
class EngineBlock(EquipmentBlock):
    MaxAccelerate: int
    Type = EquipmentType.Engine


@dataclass
class GunBlock(EquipmentBlock):
    Damage: int
    EffectType: EffectType
    EnergyPrice: int
    Radius: int
    Type = EquipmentType.Gun


@dataclass
class HealthBlock(EquipmentBlock):
    MaxHealth: int
    StartHealth: int


@dataclass
class EffectType(EquipmentBlock):
    MaxHealth: int
    StartHealth: int
    Type = EquipmentType.Health


# endregion

# region battle state

@dataclass
class Ship(JSONCapability):
    Id: int
    Position: Vector
    Velocity: Vector
    Move_vector: Vector
    Attack_vector: Vector
    Next_iteration_ship_points: dict
    Default_dangerous_ships: list = None
    Energy: Optional[int] = None
    Health: Optional[int] = None
    Equipment: dict = None

    @classmethod
    def from_json(cls, data):
        if data.get('Equipment'):
            data['Equipment'] = {
                EquipmentType(block['Type']): EquipmentBlock.from_json(block)
                for block in data.get('Equipment', [])
            }
        data['Position'] = Vector.from_json(data['Position'])
        data['Velocity'] = Vector.from_json(data['Velocity'])
        data['Move_vector'] = data['Position']
        data['Attack_vector'] = data['Position']

        # Fill next_iteration_ship_points:
        cords = data['Position'].get_cords()
        st_p = cords[0] - 1, cords[1] - 1, cords[2] - 1
        row_1 = tuple((st_p[0] + n, st_p[1], st_p[2]) for n in range(3))
        stack_1 = tuple((p[0], p[1] + n, p[2]) for n in range(3) for p in row_1)
        cube = tuple((p[0], p[1], p[2] + n) for n in range(3) for p in stack_1)
        data['Next_iteration_ship_points'] = {p: 0 for p in cube}
        data['Next_iteration_ship_points'][data['Position'].get_cords()] -= 1

        return cls(**data)

    def add_default_dangerous_ships(self, enemy_list: list):
        self.Default_dangerous_ships = BattleState.get_dangerous_ships(
            self.Position.get_cords(), enemy_list, trigger_dist=5)

    def add_correct_move(self, target: Vector):
        self.Move_vector = Vector(*bresenham_3d(
            self.Position.get_cords(), target.get_cords(), max_iter=2)[-1])

    def add_correct_target(self, target_pos: Vector, target_vil: Vector):
        pass


@dataclass
class FireInfo(JSONCapability):
    EffectType: EffectType
    Source: Vector
    Target: Vector

    @classmethod
    def from_json(cls, data):
        data['Source'] = Vector.from_json(data['Source'])
        data['Target'] = Vector.from_json(data['Target'])
        return cls(**data)


@dataclass
class BattleState(JSONCapability):
    FireInfos: List[FireInfo]
    My: List[Ship]
    Opponent: List[Ship]
    Ships_collision_pos: dict
    Ships_id_dict: dict

    @classmethod
    def from_json(cls, data):
        my = list(map(Ship.from_json, data['My']))
        opponent = list(map(Ship.from_json, data['Opponent']))
        ships_id_dict = {ship.Id: ship for ship in my + opponent}
        fire_infos = list(map(FireInfo.from_json, data['FireInfos']))

        # Fill default_dangerous_ships values
        for f_ship in my:
            f_ship.add_default_dangerous_ships(opponent)
        for e_ship in opponent:
            e_ship.add_default_dangerous_ships(my)

        ships_collision_pos = {
            ship.Id: cls.get_all_blocks_pos(ship.Position.get_cords())
            for ship in my + opponent
        }

        return cls(fire_infos, my, opponent, ships_collision_pos, ships_id_dict)

    @staticmethod
    def get_all_blocks_pos(s_cords: tuple, level: int = 0) -> tuple:
        st_p = s_cords[0] - level, s_cords[1] - level, s_cords[2] - level
        row_1 = tuple((st_p[0] + n, st_p[1], st_p[2]) for n in range((level + 1) * 2))
        stk_1 = tuple((p[0], p[1] + n, p[2]) for n in range((level + 1) * 2) for p in row_1)
        res_s = tuple((p[0], p[1], p[2] + n) for n in range((level + 1) * 2) for p in stk_1)
        return res_s

    @staticmethod
    def get_interacting_blocks(ship_1_cords, ship_2_cords) -> tuple:
        ship_1_collision_pos = BattleState.get_all_blocks_pos(ship_1_cords)
        ship_2_collision_pos = BattleState.get_all_blocks_pos(ship_2_cords)
        closest_ship_1_point = min(
            [(point, chebyshev_distance(point, ship_2_cords))
             for point in ship_1_collision_pos], key=lambda p: p[1])[0]
        closest_ship_2_point = min(
            [(point, chebyshev_distance(point, closest_ship_1_point))
             for point in ship_2_collision_pos], key=lambda p: p[1])[0]
        return closest_ship_1_point, closest_ship_2_point

    @staticmethod
    def get_distance_ships(ship_1_cords: tuple, ship_2_cords: tuple) -> int:
        ship_1_collision_pos = BattleState.get_all_blocks_pos(ship_1_cords)
        ship_2_collision_pos = BattleState.get_all_blocks_pos(ship_2_cords)
        closest_ship_1_point = min(
            [(point, chebyshev_distance(point, ship_2_cords))
             for point in ship_1_collision_pos], key=lambda p: p[1])[0]
        res_chebyshev_distance = min(
            [chebyshev_distance(point, closest_ship_1_point)
             for point in ship_2_collision_pos]) - 1
        return res_chebyshev_distance

    @staticmethod
    def get_coordinate_line(ship_1_cords, ship_2_cords, inc_dr_axis=0, max_iter=32) -> list:
        closest_ship_1_point, closest_ship_2_point = \
            BattleState.get_interacting_blocks(ship_1_cords, ship_2_cords)
        cords_list = bresenham_3d(
            closest_ship_1_point, closest_ship_2_point,
            inc_dr_axis, max_iter)
        return cords_list

    @staticmethod
    def get_dangerous_ships(ship_cords: tuple, enemies_list: list, trigger_dist=5):
        enemy_distances = \
            [(e_ship, BattleState.get_distance_ships(
                ship_cords, e_ship.Position.get_cords()))
             for e_ship in enemies_list]
        dangerous_ships = sorted(filter(
            lambda ship: ship[1] < trigger_dist, enemy_distances),
            key=lambda ship: ship[1])
        return dangerous_ships

    @staticmethod
    def get_nearest_enemy(ship_cords: tuple, enemy_ships_list: list) -> tuple:
        return min(map(lambda e_s: (
            e_s, BattleState.get_distance_ships(
                ship_cords, e_s.Position.get_cords())), enemy_ships_list),
                   key=lambda s: s[1])


# endregion


def make_draft(data: dict) -> dict:
    # TODO: parse input data
    # TODO: Make draft
    ship = list(filter(lambda s: s["Id"].lower() == 'starstorm', data['CompleteShips']))[0]
    money = data["Money"]
    count_ship = money // ship['Price']
    if count_ship > data["MaxShipsCount"]:
        count_ship = data["MaxShipsCount"]
    ships = [ship['Id']] * count_ship
    output_ships = [{"CompleteShipId": s_id} for s_id in ships]

    output = {
        "Ships": output_ships,
        "Message": str(output_ships)
    }
    return output


def make_turn(data: dict) -> BattleOutput:
    move_selection_weights_dict = {
        'non_stop_weight': -1,
        'background_weight_coefficient': 2,
        'allies_focused_weight_coefficient': 2,
        'enemy_distance_weights': {
            "small": -1,
            "medium": 4,
            "large": 2,
            "neutral": 2
        },
        'enemy_con_weight_coefficient': 2,
        'allies_distance_weight': {
            "small": 0,
            "medium": 1,
            "large": 1
        },
        'friendly_fire__weights': {
            'friendly_fire_true': 1,
            'f_f_enemy_focused': 1,
            'ally_ship_targets': 1
        }
    }

    battle_state = BattleState.from_json(data)
    battle_output = BattleOutput()
    battle_output.UserCommands = []

    # Forming move commands cycle:
    for cur_my_ship in battle_state.My:  # we could sort it
        cur_my_ship.Next_iteration_ship_points[cur_my_ship.Position.get_cords()] += \
            move_selection_weights_dict['non_stop_weight']

        # TODO FIXING BUG
        for possible_pos in cur_my_ship.Next_iteration_ship_points.keys():
            enemy_distance_weight = 0
            closest_enemy = min(
                battle_state.My, key=lambda e_s: battle_state.get_distance_ships(
                    possible_pos, e_s.Position.get_cords()))
            closest_enemy_distance = battle_state.get_distance_ships(
                possible_pos, closest_enemy.Position.get_cords())

            for possible_pos in cur_my_ship.Next_iteration_ship_points.keys():
                # Check background
                if not all(map(lambda n: 0 <= possible_pos[n] <= 28, range(3))):
                    cur_my_ship.Next_iteration_ship_points[possible_pos] += -1000
                else:
                    weight_background_coefficient = \
                        move_selection_weights_dict['background_weight_coefficient']
                    check_background_weight = -6
                    n_min, n_max = 0, 28
                    while check_background_weight:
                        n_min, n_max = n_min + 1, n_max - 1
                        check_background_weight += 1
                        if not all(map(lambda n: n_min <= possible_pos[n] <= n_max, range(3))):
                            cur_my_ship.Next_iteration_ship_points[possible_pos] += \
                                check_background_weight * weight_background_coefficient
                            add_message(str(check_background_weight * weight_background_coefficient))
                            break

            # Add weight: enemy focused distance
            enemy_focused_weight = 0
            gun_radius = cur_my_ship.Equipment[EquipmentType.Gun].Radius
            foc_dangerous_ships = battle_state.get_dangerous_ships(
                possible_pos, battle_state.Opponent, trigger_dist=gun_radius)
            if foc_dangerous_ships:  # allies focused target count
                for e_ship, _ in foc_dangerous_ships:
                    enemy_dangerous_ships = e_ship.Default_dangerous_ships
                    if enemy_dangerous_ships:
                        enemy_dangerous_ships_ids = \
                            tuple(map(lambda f_s: f_s[0].Id, enemy_dangerous_ships))
                        if cur_my_ship.Id in enemy_dangerous_ships_ids:
                            my_ship_index = enemy_dangerous_ships_ids.index(cur_my_ship.Id)
                            del enemy_dangerous_ships[my_ship_index]
                        if len(enemy_dangerous_ships_ids) > enemy_focused_weight:
                            enemy_focused_weight = len(enemy_dangerous_ships)
                allies_focused_coefficient = \
                    move_selection_weights_dict['allies_focused_weight_coefficient']
                enemy_focused_weight *= allies_focused_coefficient
                cur_my_ship.Next_iteration_ship_points[possible_pos] += \
                    enemy_focused_weight

            # Add weights: enemy distance
            enemy_distance_weight = 0
            closest_enemy = min(
                battle_state.My, key=lambda e_s: battle_state.get_distance_ships(
                    possible_pos, e_s.Position.get_cords()))
            closest_enemy_distance = battle_state.get_distance_ships(
                possible_pos, closest_enemy.Position.get_cords())
            if closest_enemy_distance in (0, 1):
                enemy_distance_weight = move_selection_weights_dict[
                    'enemy_distance_weights']['small']
            elif closest_enemy_distance in (2, 3):
                enemy_distance_weight = move_selection_weights_dict[
                    'enemy_distance_weights']['medium']
            elif closest_enemy_distance == 5:
                enemy_distance_weight = move_selection_weights_dict[
                    'enemy_distance_weights']['large']
            else:
                if closest_enemy_distance < battle_state.get_distance_ships(
                        cur_my_ship.Position.get_cords(), closest_enemy.Position.get_cords()):
                    enemy_distance_weight = move_selection_weights_dict[
                        'enemy_distance_weights']['neutral']
            cur_my_ship.Next_iteration_ship_points[possible_pos] += \
                enemy_distance_weight

            # Add weights: enemy concentration count
            con_dangerous_ships = battle_state.get_dangerous_ships(
                possible_pos, battle_state.Opponent, trigger_dist=5)
            weight_enemy_con_coefficient = \
                move_selection_weights_dict['enemy_con_weight_coefficient']
            weight_enemy_concentration = -(len(con_dangerous_ships) - 1) * weight_enemy_con_coefficient \
                if con_dangerous_ships else 0
            cur_my_ship.Next_iteration_ship_points[possible_pos] += \
                weight_enemy_concentration

            # Add weights: allies distance
            allies_distance_weight = move_selection_weights_dict[
                    'enemy_distance_weights']['large']
            if len(battle_state.My) > 1:
                closest_allies_distance = min(
                    battle_state.My, key=lambda f_s: battle_state.get_distance_ships(
                        possible_pos, f_s.Position.get_cords()))
                if closest_allies_distance in (0,):
                    allies_distance_weight = move_selection_weights_dict[
                        'enemy_distance_weights']['small']
                elif closest_enemy_distance in (1, 2):
                    allies_distance_weight = move_selection_weights_dict[
                        'enemy_distance_weights']['medium']
            cur_my_ship.Next_iteration_ship_points[possible_pos] += \
                allies_distance_weight

    # Final forming move commands:
    ship_pos_dict = {cur_my_ship.Id: max(
        cur_my_ship.Next_iteration_ship_points.items(),
        key=lambda p: p[1])[0] for cur_my_ship in battle_state.My}
    blaster_ray_collisions_dict = {
        e_ship.Id: list() for e_ship in battle_state.Opponent
    }
    for f_ship in battle_state.My:
        for e_ship in f_ship.Default_dangerous_ships:
            blaster_ray_cords = tuple(battle_state.get_coordinate_line(
                *battle_state.get_interacting_blocks(
                    f_ship.Position.get_cords(),
                    e_ship[0].Position.get_cords()))[1:])
            blaster_ray_collisions_dict[e_ship[0].Id].append(
                (f_ship, blaster_ray_cords))
    were_changes = True
    while were_changes:  # Check friendly fire positions
        were_changes = False
        for cur_my_ship in battle_state.My:
            cur_my_ship_col = battle_state.get_all_blocks_pos(ship_pos_dict[cur_my_ship.Id])
            for e_ship_id, f_ship_blaster_ray_cords_set in blaster_ray_collisions_dict.items():
                for f_ship, blaster_ray_cords in f_ship_blaster_ray_cords_set:
                    if cur_my_ship.Id == f_ship.Id:
                        continue
                    sum_a_cords = blaster_ray_cords + tuple(cur_my_ship_col)
                    if len(set(sum_a_cords)) != len(sum_a_cords):
                        friendly_fire_true = -1 * move_selection_weights_dict[
                            'friendly_fire__weights']['friendly_fire_true']
                        f_f_enemy_focused = -1 * move_selection_weights_dict[
                            'friendly_fire__weights']['f_f_enemy_focused']
                        ally_ship_targets = \
                            len(cur_my_ship.Default_dangerous_ships) * move_selection_weights_dict[
                                'friendly_fire__weights']['ally_ship_targets']
                        friendly_fire_positions_weight = \
                            friendly_fire_true + f_f_enemy_focused + ally_ship_targets
                        cur_my_ship.Next_iteration_ship_points[
                            ship_pos_dict[cur_my_ship.Id]] += friendly_fire_positions_weight
            last_weight = ship_pos_dict[cur_my_ship.Id]
            ship_pos_dict[cur_my_ship.Id], _ = max(
                cur_my_ship.Next_iteration_ship_points.items(),
                key=lambda p: p[1])
            if last_weight != ship_pos_dict[cur_my_ship.Id]:
                were_changes = True
                break
    were_changes = True
    while were_changes:  # Check the allies distance to prevent a collision
        were_changes = False
        for cur_my_ship in battle_state.My:
            cur_my_ship_col = battle_state.get_all_blocks_pos(
                ship_pos_dict[cur_my_ship.Id])
            for friendly_ship in battle_state.My:
                if friendly_ship.Id != cur_my_ship.Id:
                    sum_a_cords = tuple(set(
                        battle_state.get_all_blocks_pos(ship_pos_dict[friendly_ship.Id]) +
                        battle_state.get_all_blocks_pos(friendly_ship.Position.get_cords()))) + \
                                  cur_my_ship_col
                    if len(set(sum_a_cords)) != len(sum_a_cords):
                        cur_my_ship.Next_iteration_ship_points[
                            ship_pos_dict[cur_my_ship.Id]] += -100
                        ship_pos_dict[cur_my_ship.Id], _ = max(
                            cur_my_ship.Next_iteration_ship_points.items(),
                            key=lambda p: p[1])
                        were_changes = True
                        break
    for ship in battle_state.My:
        ship.Move_vector = Vector(*ship_pos_dict[ship.Id])

    for ship in battle_state.My:
        print(ship.Id, ship.Position.get_cords(), ship_pos_dict[ship.Id])
        pos_l = list(ship.Next_iteration_ship_points.items())
        pprint_pos_list = [pos_l[n: n + 3] for n in range(0, len(pos_l), 3)]
        print(*pprint_pos_list, sep='\n')

    # Forming command attack:
    my_ship_collision = {
        f_ship.Id: battle_state.get_all_blocks_pos(ship_pos_dict[f_ship.Id])
        for f_ship in battle_state.My
    }
    op_ships_focused = {e_ship.Id: set() for e_ship in battle_state.Opponent}
    my_ships_targets = {f_ship.Id: set() for f_ship in battle_state.My}
    for cur_my_ship in battle_state.My:
        gun_radius = cur_my_ship.Equipment[EquipmentType.Gun].Radius
        for e_ship, _ in battle_state.get_dangerous_ships(
                cur_my_ship.Position.get_cords(), battle_state.Opponent,
                trigger_dist=gun_radius):
            blaster_ray_cords = tuple(battle_state.get_coordinate_line(
                *battle_state.get_interacting_blocks(
                    ship_pos_dict[cur_my_ship.Id], e_ship.Position.get_cords()))[1:])
            my_ship_ids = set(my_ship_collision.keys())
            my_ship_ids.remove(cur_my_ship.Id)
            allies_collisions = tuple()
            for f_ship_id in my_ship_ids:
                allies_collisions += my_ship_collision[f_ship_id]
            # Check friendly fire
            if len(set(blaster_ray_cords + allies_collisions)) == \
                    len(blaster_ray_cords + allies_collisions):
                op_ships_focused[e_ship.Id].add(cur_my_ship.Id)
                my_ships_targets[cur_my_ship.Id].add(e_ship.Id)
    while any(op_ships_focused.values()):
        sorted_op_ships_focused = [
            (e_ship_id, len(f_ships), sum(map(
                lambda f_s: battle_state.get_distance_ships(
                    battle_state.Ships_id_dict[e_ship_id].Position.get_cords(),
                    ship_pos_dict[f_s]), f_ships)) / len(f_ships) if f_ships else 30)
            for e_ship_id, f_ships in op_ships_focused.items()]
        sorted_op_ships_focused.sort(key=lambda elem: (elem[1], elem[2]), reverse=True)
        sorted_op_ships_focused = list(map(
            lambda elem: (elem[0], op_ships_focused[elem[0]]), sorted_op_ships_focused))
        for e_ship_id, f_ships in sorted_op_ships_focused:
            if f_ships:
                for f_ship_id in list(f_ships):
                    f_ship = battle_state.Ships_id_dict[f_ship_id]
                    e_ship = battle_state.Ships_id_dict[e_ship_id]
                    f_ship.Attack_vector = e_ship.Position
                    for e_ship_id_2, _ in sorted_op_ships_focused:
                        if f_ship_id in op_ships_focused[e_ship_id_2]:
                            op_ships_focused[e_ship_id_2].remove(f_ship_id)
                break

    # Final formation main part output:
    for cur_my_ship in battle_state.My:
        battle_output.UserCommands.append(
            UserCommand(Command="MOVE", Parameters=MoveCommandParameters(
                cur_my_ship.Id, cur_my_ship.Move_vector)))
        if EquipmentType.Gun in cur_my_ship.Equipment.keys():
            if cur_my_ship.Attack_vector.get_cords() not in (
                    cur_my_ship.Position.get_cords(), cur_my_ship.Move_vector.get_cords()):
                battle_output.UserCommands.append(
                    UserCommand(Command="ATTACK", Parameters=AttackCommandParameters(
                        cur_my_ship.Id, cur_my_ship.Equipment[
                            EquipmentType.Gun].Name, cur_my_ship.Attack_vector)))

    # Add debugging message in output
    battle_output.Message = f"To battle..."
    for message in messages:
        if (len(message) + len(battle_output.Message)) < 3000:
            battle_output.Message += message
            continue
        break
    messages.clear()

    return battle_output


def local_test_game():
    while True:
        raw_line = 'BattleState_for_test.json'
        with open(raw_line, 'r', encoding='utf8') as json_file:
            f = json_file.read()
            line = json.loads(f)
        if 'PlayerId' in line:
            print(json.dumps(make_draft(line), default=lambda x: x.to_json(), ensure_ascii=False))
        elif 'My' in line:
            import time
            start_time = time.time()
            make_turn(line)
            print("--- %s seconds ---" % (time.time() - start_time))
            # json_output = json.dumps(output, default=lambda x: x.to_json(), ensure_ascii=False)
        input()


def play_game():
    while True:
        raw_line = input()
        line = json.loads(raw_line)
        if 'PlayerId' in line:
            print(make_draft(line))
        elif 'My' in line:
            print(json.dumps(make_turn(line), default=lambda x: x.to_json(), ensure_ascii=False))


if __name__ == '__main__':
    local_test_game()
