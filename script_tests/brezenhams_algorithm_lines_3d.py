from brezenhams_algorithm_lines_2d import get_br_cords


def get_br_cords_3d(x0, y0, z0, x1, y1, z1, x_step: int = 0) -> list:
    res_cords = []
    cords_2d_y = get_br_cords(x0, y0, x1, y1, x_step)
    cords_2d_z = get_br_cords(x0, z0, x1, z1, x_step)
    for p_y in reversed(cords_2d_y):
        for n_z in range(len(cords_2d_z) - 1, -1, -1):
            if cords_2d_z[n_z][0] == p_y[0]:
                res_cords.append((p_y[0], p_y[1], cords_2d_z.pop(n_z)[1]))
            else:
                break
    res_cords.reverse()
    return res_cords


field_size = 30
# 21, 27, 27
# 1, 3, 3

in_x0, in_y0, in_z0 = 1, 12, 6
in_x1, in_y1, in_z1 = 10, 19, 16
x_inc = 3

field = [['0(00)'] * field_size for _ in range(field_size)]

field[in_y0][in_x0] = '-2(0)'
field[in_y1][in_x1] = '-3(0)'

res = get_br_cords_3d(
    in_x0, in_y0, in_z0,
    in_x1, in_y1, in_z1, x_inc
)
s_true, e_true = False, False
print((in_x0, in_y0, in_z0), (in_x1, in_y1, in_z1), x_inc)
print(res)
for point_x, point_y, point_z in res:
    field[point_y][point_x] = f"1({str(point_z).rjust(2, '0')})"
    if (point_x, point_y, point_z) == (in_x0, in_y0, in_z0):
        s_true = True
    if (point_x, point_y, point_z) == (in_x1, in_y1, in_z1):
        e_true = True
field[in_y0][in_x0] = f"2({str(in_z0).rjust(2, '0')})"
field[in_y1][in_x1] = f"3({str(in_z1).rjust(2, '0')})"
print(s_true, e_true)
print(*field, sep='\n')
print('\n')

field_size = 30
field = [[0] * field_size for _ in range(field_size)]
in_x0, in_y0 = in_x0, in_y0
in_x1, in_y1 = in_x1, in_y1
res = get_br_cords(in_x0, in_y0, in_x1, in_y1, x_inc)
print((in_x0, in_y0), (in_x1, in_y1), x_inc, 'x, y')
print(res)
for point_x, point_y in res:
    if 0 <= point_x < field_size and 0 <= point_y < field_size:
        field[point_y][point_x] = 1
        if (point_x, point_y) == (in_x0, in_y0):
            field[point_y][point_x] = 2
        if (point_x, point_y) == (in_x1, in_y1):
            field[point_y][point_x] = 3
print(*field, sep='\n')
print('\n')

field_size = 30
field = [[0] * field_size for _ in range(field_size)]
in_x0, in_y0 = in_x0, in_z0
in_x1, in_y1 = in_x1, in_z1
res = get_br_cords(in_x0, in_y0, in_x1, in_y1, x_inc)
print((in_x0, in_y0), (in_x1, in_y1), x_inc, 'x, z')
print(res)
for point_x, point_y in res:
    if 0 <= point_x < field_size and 0 <= point_y < field_size:
        field[point_y][point_x] = 1
        if (point_x, point_y) == (in_x0, in_y0):
            field[point_y][point_x] = 2
        if (point_x, point_y) == (in_x1, in_y1):
            field[point_y][point_x] = 3
print(*field, sep='\n')
print('\n')

field_size = 30
field = [[0] * field_size for _ in range(field_size)]
in_x0, in_y0 = in_y0, in_z0
in_x1, in_y1 = in_y1, in_z1
res = get_br_cords(in_x0, in_y0, in_x1, in_y1, x_inc)
print((in_x0, in_y0), (in_x1, in_y1), x_inc, 'y, z')
print(res)
for point_x, point_y in res:
    if 0 <= point_x < field_size and 0 <= point_y < field_size:
        field[point_y][point_x] = 1
        if (point_x, point_y) == (in_x0, in_y0):
            field[point_y][point_x] = 2
        if (point_x, point_y) == (in_x1, in_y1):
            field[point_y][point_x] = 3
print(*field, sep='\n')
print('\n')


'''
(10, 18, 14) (10, 19, 16) 0
[(10, 19, 14), (10, 19, 15), (10, 19, 16)]
False True

(10, 18) (10, 19) 0 x, y
[(10, 18), (10, 19)]

(10, 14) (10, 16) 0 x, z
[(10, 14), (10, 15), (10, 16)]

(14, 14) (16, 16) 0 y, z
[(14, 14), (15, 15), (16, 16)]
'''
