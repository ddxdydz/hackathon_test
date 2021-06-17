import json
from dataclasses import dataclass
from enum import Enum
from typing import List, Optional


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

    @classmethod
    def from_list(cls, data):
        x, y, z = data
        return cls(x, y, z)

    def get_cords(self) -> tuple:
        return self.X, self.Y, self.Z

    def __str__(self):
        return f"{self.X}/{self.Y}/{self.Z}"


def get_br_cords(x0: int, y0: int, x1: int, y1: int, x_inc: int = 0) -> list:
    x_inc += 1  # increment so that the last coordinate is in the list
    res_cords, reverse = [], False
    delta_x, delta_y = abs(x1 - x0), abs(y1 - y0)
    if delta_y > delta_x:
        delta_x, delta_y = delta_y, delta_x
        x0, y0 = y0, x0
        x1, y1 = y1, x1
        reverse = True
    error, delta_err, y = 0, (delta_y + 1), y0
    dir_y = 1 if y1 - y0 > 0 else -1
    step = 1 if x1 - x0 > 0 else -1
    for x in range(x0, x1 + step * x_inc, step):
        res_cords.append((y, x) if reverse else (x, y))
        error = error + delta_err
        if error >= (delta_x + 1):
            y = y + dir_y
            error = error - (delta_x + 1)
    return res_cords


def get_br_cords_3d(x0, y0, z0, x1, y1, z1, x_inc: int = 0) -> list:
    res_cords = []
    cords_2d_y = get_br_cords(x0, y0, x1, y1, x_inc)
    cords_2d_z = get_br_cords(x0, z0, x1, z1, x_inc)
    for p_y in reversed(cords_2d_y):
        for n_z in range(len(cords_2d_z) - 1, -1, -1):
            if cords_2d_z[n_z][0] == p_y[0]:
                res_cords.append((p_y[0], p_y[1], cords_2d_z.pop(n_z)[1]))
            else:
                break
    res_cords.reverse()
    return res_cords


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
        cords = get_br_cords_3d(
            *ship_1.get_center_absolute_cords(),
            *ship_2.get_center_absolute_cords()
        )
        return len(cords) - 2

    @staticmethod
    def get_coordinate_line(ship_1: Ship, ship_2: Ship, x_inc: int = 0) -> list:
        cords_list = get_br_cords_3d(
            *ship_1.get_center_absolute_cords(),
            *ship_2.get_center_absolute_cords(),
            x_inc)
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
            'enemies': [],
            'message': ''
        }

        sorted_enemy_list = []
        for enemy_ship in self.Opponent:
            sorted_enemy_list.append(
                (enemy_ship, self.get_distance_ships(enemy_ship, my_ship))
            )
        sorted_enemy_list.sort(key=lambda elem: elem[1])
        enemy_distance_by_ship['enemies'] = sorted_enemy_list
        enemy_distance_by_ship['message'] = \
            f'FUNC get_sorted_enemies_dist_by_ship: \n' + \
            f'Ship: {my_ship}, \n' + \
            f'enemies: {enemy_distance_by_ship["enemies"]}\n'

        return enemy_distance_by_ship


# endregion


def make_draft(data: dict) -> DraftChoice:
    # TODO: parse input data
    # TODO: Make draft
    return DraftChoice()


def make_turn(data: dict) -> BattleOutput:
    battle_state = BattleState.from_json(data)

    battle_output = BattleOutput()
    battle_output.UserCommands = []
    battle_output.Message = \
        f"I have {len(battle_state.My)} ships and move to center of galaxy and shoot"

    enemy_targets_dict = {enemy.Id: [] for enemy in battle_state.Opponent}

    for cur_friendly_ship in battle_state.get_sorted_my_ships():
        sorted_enemies_dist = battle_state.get_sorted_enemies_dist_by_ship(cur_friendly_ship)
        target_enemy, target_enemy_distance =  sorted_enemies_dist['enemies'][0]
        enemy_targets_dict[target_enemy.Id].append(cur_friendly_ship)
        dangerous_enemy = cur_friendly_ship.get_dangerous_enemy(sorted_enemies_dist)

        cur_friendly_ship.move_vector = cur_friendly_ship.Position  # set default value move
        cur_friendly_ship.attack_vector = target_enemy.Position  # set default value attack

        if dangerous_enemy:
            cur_friendly_ship.move_vector = battle_state.get_coordinate_line(
                cur_friendly_ship, dangerous_enemy, 1)[-1]
        else:
            if target_enemy_distance > 5:
                cur_friendly_ship.move_vector = target_enemy.Position
            elif target_enemy_distance < 4:
                cur_friendly_ship.move_vector = Vector.from_list(battle_state.get_coordinate_line(
                    cur_friendly_ship, target_enemy, 1)[-1])
                battle_output.Message += f'\n {cur_friendly_ship} - {cur_friendly_ship.move_vector}'
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
                    cur_friendly_ship.Id, cur_friendly_ship.move_vector)
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
