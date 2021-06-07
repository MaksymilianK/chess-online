from shared.chess_engine.position import Vector2d, centre, distance_x, distance_y


def test_eq():
    assert Vector2d(1, 5) == Vector2d(1, 5)
    assert Vector2d(1, 5) != Vector2d(1, 4)
    assert Vector2d(1, 5) != Vector2d(2, 5)
    assert Vector2d(1, 5) != Vector2d(-1, -5)

def test_neg():
    assert -Vector2d(1, 5) == Vector2d(-1, -5)
    assert -Vector2d(-1, -5) == Vector2d(1, 5)

def test_add():
    assert Vector2d(1, 5) + Vector2d(-4, 6) == Vector2d(-3, 11)

def test_sub():
    assert Vector2d(1, 5) - Vector2d(-4, 6) == Vector2d(5, -1)

def test_mul():
    assert Vector2d(1, 5) * 3 == Vector2d(3, 15)

def test_rmul():
    assert 3 * Vector2d(1, 5) == Vector2d(3, 15)

def test_floordiv():
    assert Vector2d(3, 15) // 3 == Vector2d(1, 5)

def test_str():
    assert Vector2d(3, 5).__str__() == "(3, 5)"

def test_x():
    assert Vector2d(1, 5).x == 1

def test_y():
    assert Vector2d(1, 5).y == 5

def test_upper():
    assert Vector2d(1, 5).upper() == Vector2d(1, 6)

def test_upper_right():
    assert Vector2d(1, 5).upper_right() == Vector2d(2, 6)

def test_right():
    assert Vector2d(1, 5).right() == Vector2d(2, 5)

def test_bottom_right():
    assert Vector2d(1, 5).bottom_right() == Vector2d(2, 4)

def test_bottom():
    assert Vector2d(1, 5).bottom() == Vector2d(1, 4)

def test_bottom_left():
    assert Vector2d(1, 5).bottom_left() == Vector2d(0, 4)

def test_left():
    assert Vector2d(1, 5).left() == Vector2d(0, 5)

def test_upper_left():
    assert Vector2d(1, 5).upper_left() == Vector2d(0, 6)

def test_centre():
    assert centre(Vector2d(1, 5), Vector2d(-1, -5)) == Vector2d(0, 0)
    assert centre(Vector2d(1, 5), Vector2d(2, 2)) == Vector2d(1, 3)

def test_distance_x():
    assert distance_x(Vector2d(-1, 5), Vector2d(4, 5)) == 5

def test_distance_y():
    assert distance_y(Vector2d(1, -4), Vector2d(2, 7)) == 11
