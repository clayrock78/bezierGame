from math import *
from functools import cache
from pygame import Vector2

@cache
def ccos(radians):
    return cos(radians)


@cache
def csin(radians):
    return sin(radians)


def linear_parametric_2d(pos1: Vector2, pos2: Vector2, t: float) -> Vector2:
    x_pos = pos1.x * t + pos2.x * (1 - t)
    y_pos = pos1.y * t + pos2.y * (1 - t)
    return Vector2(x_pos, y_pos)


def bezier_calc_2d(curve: tuple[Vector2, Vector2, Vector2], t: float) -> Vector2:
    #print(curve)
    p0, p1, p2 = curve
    return Vector2(
        ((1 - t) ** 2) * p0.x + 2 * t * (1 - t) * p1.x + t ** 2 * p2.x,
        ((1 - t) ** 2) * p0.y + 2 * t * (1 - t) * p1.y + t ** 2 * p2.y,
    )


def approximate_bez_curve_len(curve: tuple[Vector2, Vector2, Vector2], iterations: int = 5):
    step_size = 1 / iterations
    current_t = 0
    location: Vector2
    prev_location = bezier_calc_2d(curve, current_t)
    result = 0
    for _ in range(iterations):
        current_t += step_size
        location = bezier_calc_2d(curve, current_t)
        result += len_linear_2d(location, prev_location)
        prev_location = location
    return result


def len_linear_2d(pos1: Vector2, pos2: Vector2) -> float:
    dx = pos1.x - pos2.x
    dy = pos1.y - pos2.y
    magnitude = pythag(dx, dy)
    return magnitude


def pythag(a: float, b: float) -> float:
    return (a ** 2 + b ** 2) ** 0.5


def rotate_point(point: Vector2, rotation_origin: Vector2, radians_rotate: float) -> Vector2:
    new_x = (
        ccos(round(radians_rotate, 2)) * (point.x - rotation_origin.x)
        - csin(round(radians_rotate, 2)) * (point.y - rotation_origin.y)
        + rotation_origin.x
    )
    new_y = (
        csin(round(radians_rotate, 2)) * (point.x - rotation_origin.x)
        + ccos(round(radians_rotate, 2)) * (point.y - rotation_origin.y)
        + rotation_origin.y
    )
    return Vector2(new_x, new_y)


def tuplesub(t1, t2):
    tn0 = t1[0] - t2[0]
    tn1 = t1[1] - t2[1]
    return Vector2(tn0, tn1)


def clip(val, maxval, minval):
    if val > maxval:
        return maxval
    elif val < minval:
        return minval
    else:
        return val
