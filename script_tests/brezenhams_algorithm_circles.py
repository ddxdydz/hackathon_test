def get_br_circle_cords(x1: int, y1: int, r) -> list:
    res_cords = []
    x, y = 0, r
    delta = 1 - 2 * r
    error = 0
    while y >= x:
        res_cords.append((x1 + x, y1 + y))
        res_cords.append((x1 + x, y1 - y))
        res_cords.append((x1 - x, y1 + y))
        res_cords.append((x1 - x, y1 - y))
        res_cords.append((x1 + y, y1 + x))
        res_cords.append((x1 + y, y1 - x))
        res_cords.append((x1 - y, y1 + x))
        res_cords.append((x1 - y, y1 - x))
        error = 2 * (delta + y) - 1
        if delta < 0 and error <= 0:
            delta += 2 * x + 1
            continue
        if delta > 0 and error > 0:
            delta -= 2 * y + 1
            continue
        delta += 2 * (x - y)
    return res_cords
