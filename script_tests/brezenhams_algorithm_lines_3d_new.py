# Python3 code for generating points on a 3-D line 
# using Bresenham's Algorithm


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


if __name__ == '__main__':
    in_x1, in_y1, in_z1 = 1, 12, 6
    in_x2, in_y2, in_z2 = 10, 19, 16
    res_point_list = bresenham_3d(
        in_x1, in_y1, in_z1, in_x2, in_y2, in_z2, inc_dr_axis=3)
    print(res_point_list)


'''
[(1, 12, 6), (1, 12, 7), (2, 12, 8), (3, 13, 9), (4, 14, 10), (5, 15, 11), (6, 16, 12), (7, 16, 13), (8, 17, 14), (9, 18, 15), (10, 19, 16)]
[(1, 12, 6), (2, 13, 7), (3, 13, 8), (4, 14, 9), (5, 15, 10), (6, 16, 11), (6, 16, 12), (7, 17, 13), (8, 18, 14), (9, 18, 15), (10, 19, 16)]

[(1, 12, 6), (2, 13, 7), (3, 13, 8), (4, 14, 9), (5, 15, 10), (6, 16, 11), (6, 16, 12), (7, 17, 13), (8, 18, 14), (9, 18, 15), (10, 19, 16), (11, 20, 17), (12, 20, 18), (13, 21, 19)]
[(1, 12, 6), (2, 13, 7), (3, 13, 8), (4, 14, 9), (5, 15, 10), (6, 16, 11), (6, 16, 12), (7, 17, 13), (8, 18, 14), (9, 18, 15), (10, 19, 16), (11, 20, 17), (12, 20, 18), (13, 21, 19)]
'''
