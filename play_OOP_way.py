import json
from dataclasses import dataclass
from enum import Enum
from typing import List, Optional

start_position_ship = {
    0: (0, 8, 4),
    1: (0, 4, 8),
    2: (6, 0, 6),
    3: (4, 8, 0),
    4: (8, 4, 0)
}
is_on_start_position = False
check_reverse = False
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
    Next_iteration_ship_points: dict[tuple: int]
    Energy: Optional[int] = None
    Health: Optional[int] = None
    Equipment: dict[EquipmentType: EquipmentBlock] = None
    Dangerous_ships: list = None

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
        data['Next_iteration_ship_points'] = {
            data['Next_iteration_ship_points'][p]: 0 for p in cube}

        return cls(**data)

    def add_dangerous_ships(self, enemies_list: list):
        enemy_distances = \
            [(e_ship, BattleState.get_distance_ships(
                self.Position.get_cords(), e_ship.Position.get_cords()))
             for e_ship in enemies_list]
        dangerous_ships = sorted(filter(
            lambda ship: ship[1] < 5, enemy_distances),
            key=lambda ship: ship[1])
        self.Dangerous_ships = dangerous_ships

    def add_correct_move(self, target: Vector):
        self.Move_vector = Vector(*bresenham_3d(
            self.Position.get_cords(), target.get_cords(), max_iter=2)[-1])

    # TODO
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
    # Predict_enemy_pos: dict

    @classmethod
    def from_json(cls, data):
        my = list(map(Ship.from_json, data['My']))
        opponent = list(map(Ship.from_json, data['Opponent']))
        fire_infos = list(map(FireInfo.from_json, data['FireInfos']))

        # Adding possible threats ships
        for m_ship in my:
            m_ship.add_dangerous_ships(opponent)
        for e_ship in opponent:
            e_ship.add_dangerous_ships(my)

        ships_collision_pos = {
            ship.Id: cls.get_all_blocks_pos(ship.Position.get_cords())
            for ship in my + opponent
        }

        # TODO IN WORK
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

        return cls(fire_infos, my, opponent, ships_collision_pos)

    @staticmethod
    def get_all_blocks_pos(s_cords: tuple, level: int = 0) -> tuple:
        st_p = s_cords[0] - level, s_cords[1] - level, s_cords[2] - level
        row_1 = tuple((st_p[0] + n, st_p[1], st_p[2]) for n in range((level + 1) * 2))
        stk_1 = tuple((p[0], p[1] + n, p[2]) for n in range((level + 1) * 2) for p in row_1)
        res_s = tuple((p[0], p[1], p[2] + n) for n in range((level + 1) * 2) for p in stk_1)
        return res_s

    @staticmethod
    # TODO TASTING FUNC
    def get_distance_ships(ship_1_cords: tuple, ship_2_cords: tuple) -> int:
        ship_1_collision_pos = BattleState.get_all_blocks_pos(ship_1_cords)
        ship_2_collision_pos = BattleState.get_all_blocks_pos(ship_2_cords)
        closest_ship_1_point = min(
            [(point, chebyshev_distance(point, ship_2_cords))
             for point in ship_1_collision_pos], key=lambda p: p[1])[0]
        res_chebyshev_distance = min(
            [chebyshev_distance(point, closest_ship_1_point)
             for point in ship_2_collision_pos])

        add_message(f'D {ship_1_cords}&{ship_2_cords}={res_chebyshev_distance}')

        return res_chebyshev_distance

    @staticmethod
    # TODO TASTING FUNC
    def get_min_attack_distance(ship_attack_cords: tuple, ship_target_cords: tuple) -> int:
        ship_1_collision_pos = BattleState.get_all_blocks_pos(ship_attack_cords)
        ship_2_collision_pos = BattleState.get_all_blocks_pos(ship_target_cords)
        closest_ship_1_point = min(
            [(point, manhattan_distance(point, ship_target_cords))
             for point in ship_1_collision_pos], key=lambda p: p[1])[0]
        res_chebyshev_distance = min(
            [manhattan_distance(point, closest_ship_1_point)
             for point in ship_2_collision_pos])

        add_message(f'C {ship_attack_cords} from {closest_ship_1_point} to {ship_target_cords}')

        return res_chebyshev_distance

    @staticmethod
    # TODO TASTING FUNC
    def get_coordinate_line(ship_1_cords, ship_2_cords, inc_dr_axis=0, max_iter=32) -> list:
        ship_1_collision_pos = BattleState.get_all_blocks_pos(ship_1_cords)
        ship_2_collision_pos = BattleState.get_all_blocks_pos(ship_2_cords)
        closest_ship_1_point = min(
            [(point, chebyshev_distance(point, ship_2_cords))
             for point in ship_1_collision_pos], key=lambda p: p[1])[0]
        closest_ship_2_point = min(
            [(point, chebyshev_distance(point, closest_ship_1_point))
             for point in ship_2_collision_pos], key=lambda p: p[1])[0]
        cords_list = bresenham_3d(
            closest_ship_1_point, closest_ship_2_point,
            inc_dr_axis, max_iter)

        add_message(f'F(cord_line)-{ship_1_cords},{ship_2_cords},{inc_dr_axis}={cords_list[-inc_dr_axis - 2:]}')

        return cords_list

    def get_sorted_my_ships(self) -> list:
        # Sort the ships according to the number of enemies around func
        return sorted(
            self.My,
            key=lambda my_ship: len(
                [1 for enemy_ship in self.Opponent
                 if self.get_distance_ships(
                    my_ship.Position.get_cords(),
                    enemy_ship.Position.get_cords()) < 6]
            )
        )

    def get_sorted_enemies_dist_by_ship(self, my_ship: Ship) -> dict:
        enemy_distance_by_ship = {
            'ship': my_ship,
            'enemies': []
        }
        sorted_enemy_list = []
        for enemy_ship in self.Opponent:
            sorted_enemy_list.append(
                (enemy_ship, self.get_distance_ships(
                    enemy_ship.Position.get_cords(),
                    my_ship.Position.get_cords()))
            )
        sorted_enemy_list.sort(key=lambda elem: elem[1])
        enemy_distance_by_ship['enemies'] = sorted_enemy_list
        return enemy_distance_by_ship


# endregion


def make_draft(data: dict) -> DraftChoice:
    # TODO: parse input data
    # TODO: Make draft
    data['u'] = 1
    return DraftChoice()


def make_turn(data: dict) -> BattleOutput:
    global start_position_ship, check_reverse, is_on_start_position
    battle_state = BattleState.from_json(data)
    battle_output = BattleOutput()
    battle_output.UserCommands = []

    # Realization of movement to a given starting position:
    if not is_on_start_position:
        # Checking occupied positions
        if all(map(lambda n_ship:
                   battle_state.My[n_ship].Position.get_cords() == start_position_ship[n_ship],
                   range(len(battle_state.My)))):
            is_on_start_position = True
        else:
            # Check Reverse
            if not check_reverse:
                if battle_state.My[0].Position.get_cords()[0] > 15:
                    start_position_ship = \
                        {key: tuple(30 - value[n] - 2 for n in range(len(value)))
                         for key, value in start_position_ship.items()}
                check_reverse = True
            # Move detection
            for num_ship, ship in enumerate(battle_state.My):
                battle_output.UserCommands.append(
                    UserCommand(Command="MOVE", Parameters=MoveCommandParameters(
                        ship.Id, Vector(*start_position_ship[num_ship]))))
            battle_output.Message = ''
            messages.clear()
            return battle_output

    # Main move commands cycle:
    for cur_my_ship in battle_state.My:  # we could sort it
        pass

        # Check the allies distance to prevent a collision
        cur_my_ship_cords = \
            battle_state.get_all_blocks_pos(cur_my_ship.Move_vector.get_cords())
        for friendly_ship in battle_state.My:
            if friendly_ship.Id != cur_my_ship.Id:
                sum_a_cords = battle_state.Ships_collision_pos[friendly_ship.Id] + cur_my_ship_cords
                if len(set(sum_a_cords)) != len(sum_a_cords):
                    break

        # Updating the battle_state.Ships_collision_pos
        battle_state.Ships_collision_pos[cur_my_ship.Id] = \
            battle_state.get_all_blocks_pos(
                cur_my_ship.Move_vector.get_cords())

    # Final formation move commands:
    # for cur_my_ship in battle_state.My:

    # Main command attack cycle:
    # for cur_my_ship in battle_state.My:

    # Final formation main part output:
    for cur_my_ship in battle_state.My:
        battle_output.UserCommands.append(
            UserCommand(Command="MOVE", Parameters=MoveCommandParameters(
                cur_my_ship.Id, cur_my_ship.Move_vector)))
        guns = [x for x in cur_my_ship.Equipment if isinstance(x, GunBlock)]
        if guns:
            battle_output.UserCommands.append(
                UserCommand(Command="ATTACK", Parameters=AttackCommandParameters(
                    cur_my_ship.Id, guns[0].Name, cur_my_ship.Attack_vector)))

    # Add debugging message in output
    battle_output.Message = ''
    for message in messages:
        if (len(message) + len(battle_output.Message)) < 4000:
            battle_output.Message += message
            continue
        break
    messages.clear()

    return battle_output


def play_game():
    while True:
        raw_line = input()
        line = json.loads(raw_line)
        if 'PlayerId' in line:
            print(json.dumps(make_draft(line), default=lambda x: x.to_json(), ensure_ascii=False))
        elif 'My' in line:
            print(json.dumps(make_turn(line), default=lambda x: x.to_json(), ensure_ascii=False))


if __name__ == '__main__':
    play_game()
