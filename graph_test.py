import json
from ursina import *

BATTLE_PATH = 'battle_20210710211759726910_dw.json'
CUR_STEP = 0
DIF = -15
CAMERA_STEP = 1

BLOCK_PLAYER_1_ID = 12341
BLOCK_PLAYER_2_ID = 41415
BLOCK_RAY_PLAYER_1_ID = 52646
BLOCK_RAY_PLAYER_2_ID = 96646
BLOCK_END_BLASTER_RAY_ID = 64212
BLOCK_TAKE_DAMAGE_ID = 53268

GAME_WINDOW_COLOR = Color(0, 0, 0, 0)
GAME_NET_COLOR = rgb(135, 135, 135, 255)
OUTLINE_GAME_NET_COLOR = rgb(255, 255, 255, 255)

BLOCK_PLAYER_1_COLOR = rgb(204, 240, 254, 255)
OUTLINE_PLAYER_1_COLOR = rgb(106, 160, 207, 255)
BLASTER_RAY_PLAYER_1_COLOR = rgb(157, 185, 224, 180)

BLOCK_PLAYER_2_COLOR = rgb(255, 231, 149, 255)
OUTLINE_PLAYER_2_COLOR = rgb(171, 103, 54, 255)
BLASTER_RAY_PLAYER_2_COLOR = rgb(255, 231, 149, 180)

BLASTER_RAY_END_COLOR = rgb(255, 0, 0, 210)
BLOCK_TAKE_DAMAGE_COLOR = rgb(255, 0, 0, 210)


def d_x(x_pos):
    return x_pos + DIF


def d_y(y_pos):
    return y_pos + DIF


def d_z(z_pos):
    return z_pos + DIF


class Game(Ursina):
    CUR_STEP = 1

    def __init__(self):
        super().__init__()
        window.title = 'my_battle_arena'
        window.color = GAME_WINDOW_COLOR
        window.borderless = False

        camera.orthographic = True
        camera.fov = 2
        EditorCamera()
        camera.world_position = (0, 0, 0)

        self.test = 0
        self.block_type_dict = {
            BLOCK_PLAYER_1_ID: Game.block_player_1,
            BLOCK_PLAYER_2_ID: Game.block_player_2,
            BLOCK_RAY_PLAYER_1_ID: Game.block_ray_blaster_1,
            BLOCK_RAY_PLAYER_2_ID: Game.block_ray_blaster_2,
            BLOCK_END_BLASTER_RAY_ID: Game.block_end_blaster,
            BLOCK_TAKE_DAMAGE_ID: Game.block_damage
        }
        with open(f'battles/{BATTLE_PATH}', 'r', encoding='utf8') as file:
            f = file.read()
            self.data = json.loads(f)
        self.load_game()

    def load_game(self):
        scene.clear()
        Game.init_game_net()
        if self.test:
            Game.block_player_1(13, 13, 13)
            Game.block_player_1(13, 14, 13)
            Game.block_player_1(13, 13, 14)
            Game.block_player_1(13, 14, 14)
            Game.block_damage(14, 13, 13)
            Game.block_player_1(14, 14, 13)
            Game.block_player_1(14, 13, 14)
            Game.block_player_1(14, 14, 14)

            Game.block_player_1(13, 13, 18)
            Game.block_player_2(13, 14, 18)
            Game.block_player_2(13, 13, 19)
            Game.block_player_2(13, 14, 19)
            Game.block_damage(14, 13, 18)
            Game.block_player_2(14, 14, 18)
            Game.block_player_2(14, 13, 19)
            Game.block_player_2(14, 14, 19)

            Game.block_ray_blaster_1(14, 14, 14)
            Game.block_ray_blaster_1(14, 15, 14)
            Game.block_ray_blaster_1(14, 16, 14)
            Game.block_ray_blaster_1(14, 17, 14)
            Game.block_end_blaster(14, 18, 14)

            Game.block_ray_blaster_2(14, 14, 19)
            Game.block_ray_blaster_2(14, 15, 19)
            Game.block_ray_blaster_2(14, 16, 19)
            Game.block_ray_blaster_2(14, 17, 19)
            Game.block_end_blaster(14, 18, 19)
            return

        for block_id, cords in self.data[str(self.CUR_STEP)]["object_positions"]:
            x, y, z = cords
            self.block_type_dict[block_id](x, y, z)
            print(self.data[str(self.CUR_STEP)]["message"])

    @staticmethod
    def init_game_net():
        for y in range(31):  # , rotation=(0, 0, 90)
            Entity(model='line', scale=30, x=d_x(15 - 0.5), y=d_y(y - 0.5), z=d_z(0 - 0.5), color=GAME_NET_COLOR)
            Entity(model='line', scale=30, x=d_x(0 - 0.5), y=d_y(y - 0.5), z=d_z(15 - 0.5), color=GAME_NET_COLOR,
                   rotation=(0, 90, 0))
        for z in range(31):
            Entity(model='line', scale=30, x=d_x(15 - 0.5), y=d_y(0 - 0.5), z=d_z(z - 0.5), color=GAME_NET_COLOR)
            Entity(model='line', scale=30, x=d_x(0 - 0.5), y=d_y(15 - 0.5), z=d_z(z - 0.5), color=GAME_NET_COLOR,
                   rotation=(0, 0, 90))
        for x in range(31):
            Entity(model='line', scale=30, x=d_x(x - 0.5), y=d_y(15 - 0.5), z=d_z(0 - 0.5), color=GAME_NET_COLOR,
                   rotation=(0, 0, 90))
            Entity(model='line', scale=30, x=d_x(x - 0.5), y=d_y(0 - 0.5), z=d_z(15 - 0.5), color=GAME_NET_COLOR,
                   rotation=(0, 90, 0))
        Entity(model='line', scale=30, x=d_x(15 - 0.5), y=d_y(30 - 0.5), z=d_z(30 - 0.5), color=OUTLINE_GAME_NET_COLOR)
        Entity(model='line', scale=30, x=d_x(15 - 0.5), y=d_y(30 - 0.5), z=d_z(0 - 0.5), color=OUTLINE_GAME_NET_COLOR)
        Entity(model='line', scale=30, x=d_x(15 - 0.5), y=d_y(0 - 0.5), z=d_z(0 - 0.5), color=OUTLINE_GAME_NET_COLOR)
        Entity(model='line', scale=30, x=d_x(30 - 0.5), y=d_y(15 - 0.5), z=d_z(30 - 0.5), color=OUTLINE_GAME_NET_COLOR,
               rotation=(0, 0, 90))
        Entity(model='line', scale=30, x=d_x(30 - 0.5), y=d_y(15 - 0.5), z=d_z(0 - 0.5), color=OUTLINE_GAME_NET_COLOR,
               rotation=(0, 0, 90))
        Entity(model='line', scale=30, x=d_x(0 - 0.5), y=d_y(15 - 0.5), z=d_z(0 - 0.5), color=OUTLINE_GAME_NET_COLOR,
               rotation=(0, 0, 90))
        Entity(model='line', scale=30, x=d_x(30 - 0.5), y=d_y(30 - 0.5), z=d_z(15 - 0.5), color=OUTLINE_GAME_NET_COLOR,
               rotation=(0, 90, 0))
        Entity(model='line', scale=30, x=d_x(15 - 0.5), y=d_y(0 - 0.5), z=d_z(30 - 0.5), color=OUTLINE_GAME_NET_COLOR)
        Entity(model='line', scale=30, x=d_x(0 - 0.5), y=d_y(15 - 0.5), z=d_z(30 - 0.5), color=OUTLINE_GAME_NET_COLOR,
               rotation=(0, 0, 90))
        Entity(model='line', scale=30, x=d_x(0 - 0.5), y=d_y(30 - 0.5), z=d_z(15 - 0.5), color=OUTLINE_GAME_NET_COLOR,
               rotation=(0, 90, 0))
        Entity(model='line', scale=30, x=d_x(0 - 0.5), y=d_y(0 - 0.5), z=d_z(15 - 0.5), color=OUTLINE_GAME_NET_COLOR,
               rotation=(0, 90, 0))
        Entity(model='line', scale=30, x=d_x(30 - 0.5), y=d_y(0 - 0.5), z=d_z(15 - 0.5), color=OUTLINE_GAME_NET_COLOR,
               rotation=(0, 90, 0))

    @staticmethod
    def block_player(x, y, z, block=BLOCK_PLAYER_1_COLOR, outline=OUTLINE_PLAYER_1_COLOR):
        Entity(model='line', scale=1, x=d_x(x), y=d_y(y + 0.5), z=d_z(z + 0.5), color=outline)
        Entity(model='line', scale=1, x=d_x(x), y=d_y(y - 0.5), z=d_z(z + 0.5), color=outline)
        Entity(model='line', scale=1, x=d_x(x), y=d_y(y - 0.5), z=d_z(z - 0.5), color=outline)
        Entity(model='line', scale=1, x=d_x(x), y=d_y(y + 0.5), z=d_z(z - 0.5), color=outline)
        Entity(model='line', scale=1, x=d_x(x - 0.5), y=d_y(y + 0.5), z=d_z(z), color=outline, rotation=(0, 90, 0))
        Entity(model='line', scale=1, x=d_x(x + 0.5), y=d_y(y + 0.5), z=d_z(z), color=outline, rotation=(0, 90, 0))
        Entity(model='line', scale=1, x=d_x(x + 0.5), y=d_y(y - 0.5), z=d_z(z), color=outline, rotation=(0, 90, 0))
        Entity(model='line', scale=1, x=d_x(x - 0.5), y=d_y(y - 0.5), z=d_z(z), color=outline, rotation=(0, 90, 0))
        Entity(model='line', scale=1, x=d_x(x - 0.5), y=d_y(y), z=d_z(z - 0.5), color=outline, rotation=(0, 0, 90))
        Entity(model='line', scale=1, x=d_x(x - 0.5), y=d_y(y), z=d_z(z + 0.5), color=outline, rotation=(0, 0, 90))
        Entity(model='line', scale=1, x=d_x(x + 0.5), y=d_y(y), z=d_z(z - 0.5), color=outline, rotation=(0, 0, 90))
        Entity(model='line', scale=1, x=d_x(x + 0.5), y=d_y(y), z=d_z(z + 0.5), color=outline, rotation=(0, 0, 90))
        Entity(model='cube', x=d_x(x), y=d_y(y), z=d_z(z), color=block)

    @staticmethod
    def block_player_1(x, y, z):
        Game.block_player(x, y, z)

    @staticmethod
    def block_player_2(x, y, z):
        Game.block_player(
            x, y, z,
            block=BLOCK_PLAYER_2_COLOR,
            outline=OUTLINE_PLAYER_2_COLOR
        )

    @staticmethod
    def block_ray_blaster_1(x, y, z):
        Entity(
            model='cube', x=d_x(x), y=d_y(y), z=d_z(z),
            color=BLASTER_RAY_PLAYER_1_COLOR
        )

    @staticmethod
    def block_ray_blaster_2(x, y, z):
        Entity(
            model='cube', x=d_x(x), y=d_y(y), z=d_z(z),
            color=BLASTER_RAY_PLAYER_2_COLOR
        )

    @staticmethod
    def block_end_blaster(x, y, z):
        Entity(
            model='cube', x=d_x(x), y=d_y(y), z=d_z(z),
            color=BLASTER_RAY_END_COLOR
        )

    @staticmethod
    def block_damage(x, y, z):
        Entity(model='cube', x=d_x(x), y=d_y(y), z=d_z(z), color=BLOCK_TAKE_DAMAGE_COLOR)

    def input(self, key):
        if key in ('w', 's', 'a', 'd', 'q', 'e'):
            camera_x, camera_y, camera_z = camera.world_position
            if key == 'w':
                camera.world_position = \
                    (camera_x + CAMERA_STEP, camera_y, camera_z)
            elif key == 'a':
                camera.world_position = \
                    (camera_x, camera_y, camera_z - CAMERA_STEP)
            elif key == 's':
                camera.world_position = \
                    (camera_x - CAMERA_STEP, camera_y, camera_z)
            elif key == 'd':
                camera.world_position = \
                    (camera_x, camera_y, camera_z + CAMERA_STEP)
            elif key == 'e':
                camera.world_position = \
                    (camera_x, camera_y + CAMERA_STEP, camera_z)
            elif key == 'q':
                camera.world_position = \
                    (camera_x, camera_y - CAMERA_STEP, camera_z)
            print(f'Camera_position - {camera.world_position}')
        if key in ('arrow_left', 'arrow_right'):
            if key == 'arrow_left':
                if self.CUR_STEP != 1:
                    self.CUR_STEP -= 1
                self.load_game()
            elif key == 'arrow_right':
                if self.CUR_STEP != len(list(self.data.keys())):
                    self.CUR_STEP += 1
                self.load_game()
        elif key == 't':
            self.test = not self.test
            self.load_game()

        super().input(key)


if __name__ == '__main__':
    game = Game()
    game.run()
