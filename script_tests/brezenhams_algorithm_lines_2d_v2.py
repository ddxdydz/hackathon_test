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


def get_br_cords_v2(x0: int, y0: int, x1: int, y1: int, x_step: int = 0) -> list:
    res_cords = []

    dx, dy = x1 - x0, y1 - y0
    sign_x = 1 if dx > 0 else -1 if dx < 0 else 0
    sign_y = 1 if dy > 0 else -1 if dy < 0 else 0

    dx = -dx if dx < 0 else dx
    dy = -dy if dy < 0 else dy

    if dx > dy:
        pdx, pdy = sign_x, 0
        es, el = dy, dx
    else:
        pdx, pdy = 0, sign_y
        es, el = dx, dy

    x, y = x0, y0

    error, t = el / 2, 0

    res_cords.append((x, y))

    while t < el:
        error -= es
        if error < 0:
            error += el
            x += sign_x
            y += sign_y
        else:
            x += pdx
            y += pdy
        t += 1
        res_cords.append((x, y))
    return res_cords


import time
start_time = time.time()
get_br_cords(1, 3, 9999, 9999)
print("--- %s seconds ---" % (time.time() - start_time))
start_time = time.time()
get_br_cords_v2(1, 3, 9999, 9999)
print("--- %s seconds ---" % (time.time() - start_time))

field_size = 10

in_x0, in_y0 = 9, 1
in_x1, in_y1 = 1, 8

for n, res in enumerate([get_br_cords(in_x0, in_y0, in_x1, in_y1), get_br_cords_v2(in_x0, in_y0, in_x1, in_y1)], 1):
    print(n, res)
    field = [[0] * field_size for _ in range(field_size)]
    field[in_y0][in_x0] = -2
    field[in_y1][in_x1] = -3
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
