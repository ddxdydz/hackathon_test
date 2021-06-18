"""x = y = z = 18
xy = zy = zx = (x ** 2 + y ** 2) ** 0.5
d = xy / 3

s = (d ** 2 / 2) ** 0.5

print(f'0: ({0}; {y - s}; {s})',
      f'1: ({s}; {y - s}; {0})',
      f'2: ({x - s}; {s}; {0})',
      f'3: ({x / 2}; {0}; {y / 2})',
      f'4: ({x - s}; {s}; {0})', sep='\n')
"""


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

