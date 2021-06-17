from brezenhams_algorithm_lines_2d import get_br_cords


def test_get_br_cords_3d(x0: int, y0: int, z0: int, x1: int, y1: int, z1: int, x_step: int = 0) -> list:
    res_cords = []
    cords_2d_y = get_br_cords(x0, y0, x1, y1, x_step)
    print(cords_2d_y)
    print(get_br_cords(x0, z0, x1, z1, x_step))
    print()
    cords_2d_z = list(map(
        lambda elem: elem[0],
        get_br_cords(x0, z0, x1, z1, x_step)
    ))

    last_z = cords_2d_z.pop(0)
    z_list = [1]
    for point in cords_2d_z:
        if point == last_z:
            z_list[-1] += 1
        else:
            z_list.append(z_list[-1] + 1)
            last_z = point

    for n in range(len(cords_2d_y)):
        res_cords.append((cords_2d_y[n][0], cords_2d_y[n][1], z_list[n]))

    print(res_cords)
    return res_cords


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


field_size = 10

in_x0, in_y0, in_z0 = 7, 2, 1
in_x1, in_y1, in_z1 = 5, 4, 8

field = [['0(0)'] * field_size for _ in range(field_size)]

field[in_y0][in_x0] = '-2(0)'
field[in_y1][in_x1] = '-3(0)'

res = get_br_cords_3d(
    in_x0, in_y0, in_z0,
    in_x1, in_y1, in_z1, 1
)
for point_x, point_y, point_z in res:
    print(point_x, point_y, point_z)
    field[point_y][point_x] = f"1({point_z})"
    if (point_x, point_y, point_z) == (in_x0, in_y0, in_z0):
        field[point_y][point_x] = f"2({point_z})"
    if (point_x, point_y, point_z) == (in_x1, in_y1, in_z1):
        field[point_y][point_x] = f"3({point_z})"
print(*field, sep='\n')
print('\n')



