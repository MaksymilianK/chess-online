from __future__ import annotations


class Vector2d:
    def __init__(self, x: int, y: int):
        self.coords = (x, y)

    @property
    def x(self) -> int:
        return self.coords[0]

    @property
    def y(self) -> int:
        return self.coords[1]

    def upper(self) -> Vector2d:
        return self + UP

    def upper_right(self) -> Vector2d:
        return self + UP_RIGHT

    def right(self) -> Vector2d:
        return self + RIGHT

    def bottom_right(self) -> Vector2d:
        return self + DOWN_RIGHT

    def bottom(self) -> Vector2d:
        return self + DOWN

    def bottom_left(self) -> Vector2d:
        return self + DOWN_LEFT

    def left(self) -> Vector2d:
        return self + LEFT

    def upper_left(self) -> Vector2d:
        return self + UP_LEFT

    def __neg__(self) -> Vector2d:
        return Vector2d(-self.x, -self.y)

    def __add__(self, other: Vector2d) -> Vector2d:
        return Vector2d(self.x + other.x, self.y + other.y)

    def __sub__(self, other: Vector2d) -> Vector2d:
        return Vector2d(self.x - other.x, self.y - other.y)

    def __mul__(self, other: int) -> Vector2d:
        return Vector2d(other * self.x, other * self.y)

    def __rmul__(self, other: int) -> Vector2d:
        return Vector2d(other * self.x, other * self.y)

    def __floordiv__(self, other: int) -> Vector2d:
        return Vector2d(self.x // other, self.y // other)

    def __eq__(self, other: Vector2d) -> bool:
        return self.x == other.x and self.y == other.y

    def __hash__(self) -> int:
        return hash(self.coords)

    def __str__(self) -> str:
        return "({}, {})".format(self.x, self.y)


def centre(pos_1: Vector2d, pos_2: Vector2d) -> Vector2d:
    return Vector2d((pos_1.x + pos_2.x) // 2, (pos_1.y + pos_2.y) // 2)


def distance_x(pos_1: Vector2d, pos_2: Vector2d) -> int:
    return abs(pos_1.x - pos_2.x)


def distance_y(pos_1: Vector2d, pos_2: Vector2d) -> int:
    return abs(pos_1.y - pos_2.y)


UP = Vector2d(0, 1)
UP_RIGHT = Vector2d(1, 1)
RIGHT = Vector2d(1, 0)
DOWN_RIGHT = Vector2d(1, -1)
DOWN = Vector2d(0, -1)
DOWN_LEFT = Vector2d(-1, -1)
LEFT = Vector2d(-1, 0)
UP_LEFT = Vector2d(-1, 1)
