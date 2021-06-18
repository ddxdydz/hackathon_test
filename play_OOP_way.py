import json
from dataclasses import dataclass
from enum import Enum
from typing import List, Optional

start_position_ship = {
    0: (0, 10, 10),
    1: (3, 10, 10),
    2: (7, 7, 8),
    3: (16, 10, 0),
    4: (16, 6, 0)
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


def bresenham_3d(x1, y1, z1, x2, y2, z2, inc_dr_axis: int = 0) -> list:
    # Python3 code for generating points on a 3-D line
    # using Bresenham's Algorithm
    res_points_list = [(x1, y1, z1)]
    dx, dy, dz = abs(x2 - x1), abs(y2 - y1), abs(z2 - z1)
    xs = 1 if x2 > x1 else -1
    ys = 1 if y2 > y1 else -1
    zs = 1 if z2 > z1 else -1

    # Driving axis is X-axis"
    if dx >= dy and dx >= dz:
        inc_dr_axis *= xs
        p1 = 2 * dy - dx
        p2 = 2 * dz - dx
        while x1 != (x2 + inc_dr_axis):
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

    # Driving axis is Y-axis"
    elif dy >= dx and dy >= dz:
        inc_dr_axis *= ys
        p1 = 2 * dx - dy
        p2 = 2 * dz - dy
        while y1 != (y2 + inc_dr_axis):
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

    # Driving axis is Z-axis"
    else:
        inc_dr_axis *= zs
        p1 = 2 * dy - dz
        p2 = 2 * dx - dz
        while z1 != (z2 + inc_dr_axis):
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

    return res_points_list


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
    Energy: Optional[int] = None
    Health: Optional[int] = None
    Equipment: List[EquipmentBlock] = None

    @classmethod
    def from_json(cls, data):
        if data.get('Equipment'):
            data['Equipment'] = list(map(EquipmentBlock.from_json, data.get('Equipment', [])))
        data['Position'] = Vector.from_json(data['Position'])
        data['Velocity'] = Vector.from_json(data['Velocity'])
        return cls(**data)

    def get_center_absolute_cords(self) -> tuple:
        x, y, z = self.Position.get_cords()
        return x + 1, y + 1, z + 1

    @staticmethod
    def get_dangerous_enemy(sorted_enemies_dist):
        if len(sorted_enemies_dist['enemies']) > 2:
            dangerous_enemy_tup = sorted_enemies_dist['enemies'][1]
            if dangerous_enemy_tup[1] < 6:
                return dangerous_enemy_tup[0]
        return False


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

    @classmethod
    def from_json(cls, data):
        my = list(map(Ship.from_json, data['My']))
        opponent = list(map(Ship.from_json, data['Opponent']))
        fire_infos = list(map(FireInfo.from_json, data['FireInfos']))
        return cls(fire_infos, my, opponent)

    @staticmethod
    def get_distance_ships(ship_1: Ship, ship_2: Ship) -> int:
        cords = bresenham_3d(
            *ship_1.get_center_absolute_cords(),
            *ship_2.get_center_absolute_cords()
        )
        res_distance = len(cords) - 2
        add_message(f'F(dist_s) - {ship_1.Id}&{ship_2.Id}={res_distance}')
        return res_distance

    @staticmethod
    def get_coordinate_line(ship_1: Ship, ship_2: Ship, x_inc: int = 0) -> list:
        cords_list = bresenham_3d(
            *ship_1.get_center_absolute_cords(),
            *ship_2.get_center_absolute_cords(),
            x_inc)
        add_message(
            f'F(cord_line)-{ship_1.Id},{ship_2.Id},{x_inc}={cords_list[-x_inc - 2:]}'
        )
        return cords_list

    def get_sorted_my_ships(self) -> list:
        '''sort the ships according to the number of enemies around'''
        return sorted(
            self.My,
            key=lambda my_ship: len(
                [1 for enemy_ship in self.Opponent
                 if self.get_distance_ships(my_ship, enemy_ship) < 6]
            ),
            reverse=True
        )

    def get_sorted_enemies_dist_by_ship(self, my_ship: Ship) -> dict:
        enemy_distance_by_ship = {
            'ship': my_ship,
            'enemies': []
        }

        sorted_enemy_list = []
        for enemy_ship in self.Opponent:
            sorted_enemy_list.append(
                (enemy_ship, self.get_distance_ships(enemy_ship, my_ship))
            )
        sorted_enemy_list.sort(key=lambda elem: elem[1])
        enemy_distance_by_ship['enemies'] = sorted_enemy_list
        return enemy_distance_by_ship


# endregion


def make_draft(data: dict) -> DraftChoice:
    # TODO: parse input data
    # TODO: Make draft
    return DraftChoice()


def make_turn(data: dict) -> BattleOutput:
    global start_position_ship, check_reverse, is_on_start_position
    battle_state = BattleState.from_json(data)

    battle_output = BattleOutput()
    battle_output.UserCommands = []
    battle_output.Message = ''

    enemy_targets_dict = {enemy.Id: [] for enemy in battle_state.Opponent}
    cur_friendly_ship_list = sorted(battle_state.My, key=lambda s: s.Id)

    if not is_on_start_position:
        if not check_reverse:
            if cur_friendly_ship_list[0].Position.get_cords()[0] > 15:
                start_position_ship = \
                    {key: tuple(30 - value[n] - 2 for n in range(len(value)))
                     for key, value in start_position_ship.items()}
            check_reverse = True
        for num_ship, ship in enumerate(cur_friendly_ship_list):
            ship.move_vector = Vector(*start_position_ship[num_ship])
        if all(map(lambda n_ship:
                   cur_friendly_ship_list[n_ship].Position.get_cords() == start_position_ship[n_ship],
                   range(len(cur_friendly_ship_list)))):
            is_on_start_position = True
    else:
        cur_friendly_ship_list = battle_state.get_sorted_my_ships()

    for cur_friendly_ship in cur_friendly_ship_list:
        sorted_enemies_dist = battle_state.get_sorted_enemies_dist_by_ship(cur_friendly_ship)
        target_enemy, target_enemy_distance = sorted_enemies_dist['enemies'][0]
        enemy_targets_dict[target_enemy.Id].append(cur_friendly_ship)
        dangerous_enemy = cur_friendly_ship.get_dangerous_enemy(sorted_enemies_dist)

        if is_on_start_position:
            cur_friendly_ship.move_vector = cur_friendly_ship.Position  # set default value move
        cur_friendly_ship.attack_vector = target_enemy.Position  # set default value attack

        if is_on_start_position:
            if isinstance(dangerous_enemy, Ship):
                cur_friendly_ship.move_vector = Vector(*battle_state.get_coordinate_line(
                    cur_friendly_ship, dangerous_enemy, 1)[-1])
            else:
                if target_enemy_distance > 5:
                    cur_friendly_ship.move_vector = target_enemy.Position
                elif target_enemy_distance < 4:
                    cur_friendly_ship.move_vector = Vector(*battle_state.get_coordinate_line(
                        cur_friendly_ship, target_enemy, 1)[-1])
                elif 4 <= target_enemy_distance < 5:
                    if len(enemy_targets_dict[target_enemy.Id]) >= 2 and \
                            min(enemy_targets_dict[target_enemy.Id][:-1],
                                key=lambda my_ship: my_ship.Health).Health < \
                            cur_friendly_ship.Health * 0.5:
                        cur_friendly_ship.move_vector = target_enemy.Position

        battle_output.UserCommands.append(
            UserCommand(
                Command="MOVE",
                Parameters=MoveCommandParameters(
                    cur_friendly_ship.Id, cur_friendly_ship.move_vector
                )
            )
        )
        guns = [x for x in cur_friendly_ship.Equipment if isinstance(x, GunBlock)]
        if guns:
            battle_output.UserCommands.append(
                UserCommand(
                    Command="ATTACK",
                    Parameters=AttackCommandParameters(
                        cur_friendly_ship.Id, guns[0].Name, cur_friendly_ship.attack_vector
                    )
                )
            )
    battle_output.Message = '\n'.join(messages)
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
