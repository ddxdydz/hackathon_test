def get_br_cords(x0: int, y0: int, x1: int, y1: int, x_step: int = 0) -> list:
    x_step += 1  # increment so that the last coordinate is in the list
    res_cords = []
    delta_x = abs(x1 - x0)
    delta_y = abs(y1 - y0)
    reverse = False
    if delta_y > delta_x:
        delta_x, delta_y = delta_y, delta_x
        x0, y0 = y0, x0
        x1, y1 = y1, x1
        reverse = True
    error = 0
    delta_err = (delta_y + 1)
    y = y0
    dir_y = 1 if y1 - y0 > 0 else -1
    step = 1 if x1 - x0 > 0 else -1
    for x in range(x0, x1 + step * x_step, step):
        res_cords.append((y, x) if reverse else (x, y))
        error = error + delta_err
        if error >= (delta_x + 1):
            y = y + dir_y
            error = error - (delta_x + 1)
    return res_cords


field_size = 10

in_x0, in_y0 = 7, 1
in_x1, in_y1 = 5, 8

field = [[0] * field_size for _ in range(field_size)]
field[in_y0][in_x0] = -2
field[in_y1][in_x1] = -3
res = get_br_cords(in_x0, in_y0, in_x1, in_y1, 1)
for point_x, point_y in res:
    field[point_y][point_x] = 1
    if (point_x, point_y) == (in_x0, in_y0):
        field[point_y][point_x] = 2
    if (point_x, point_y) == (in_x1, in_y1):
        field[point_y][point_x] = 3
field[in_y0][in_x0] = 2
field[in_y1][in_x1] = 3
print(*field, sep='\n')
print('\n')

