from shared.chess_engine.position import Vector2d, centre, distance_x, distance_y


class TestVector2d:
    def test_eq(self):
        assert Vector2d(1, 5) == Vector2d(1, 5)
        assert Vector2d(1, 5) != Vector2d(1, 4)
        assert Vector2d(1, 5) != Vector2d(2, 5)
        assert Vector2d(1, 5) != Vector2d(-1, -5)

    def test_neg(self):
        assert -Vector2d(1, 5) == Vector2d(-1, -5)
        assert -Vector2d(-1, -5) == Vector2d(1, 5)

    def test_add(self):
        assert Vector2d(1, 5) + Vector2d(-4, 6) == Vector2d(-3, 11)

    def test_sub(self):
        assert Vector2d(1, 5) - Vector2d(-4, 6) == Vector2d(5, -1)

    def test_mul(self):
        assert Vector2d(1, 5) * 3 == Vector2d(3, 15)

    def test_rmul(self):
        assert 3 * Vector2d(1, 5) == Vector2d(3, 15)

    def test_floordiv(self):
        assert Vector2d(3, 15) // 3 == Vector2d(1, 5)

    def test_str(self):
        assert Vector2d(3, 5).__str__() == "(3, 5)"

    def test_x(self):
        assert Vector2d(1, 5).x == 1

    def test_y(self):
        assert Vector2d(1, 5).y == 5

    def test_upper(self):
        assert Vector2d(1, 5).upper() == Vector2d(1, 6)

    def test_upper_right(self):
        assert Vector2d(1, 5).upper_right() == Vector2d(2, 6)

    def test_right(self):
        assert Vector2d(1, 5).right() == Vector2d(2, 5)

    def test_bottom_right(self):
        assert Vector2d(1, 5).bottom_right() == Vector2d(2, 4)

    def test_bottom(self):
        assert Vector2d(1, 5).bottom() == Vector2d(1, 4)

    def test_bottom_left(self):
        assert Vector2d(1, 5).bottom_left() == Vector2d(0, 4)

    def test_left(self):
        assert Vector2d(1, 5).left() == Vector2d(0, 5)

    def test_upper_left(self):
        assert Vector2d(1, 5).upper_left() == Vector2d(0, 6)

    def test_centre(self):
        assert centre(Vector2d(1, 5), Vector2d(-1, -5)) == Vector2d(0, 0)
        assert centre(Vector2d(1, 5), Vector2d(2, 2)) == Vector2d(1, 3)

    def test_distance_x(self):
        assert distance_x(Vector2d(-1, 5), Vector2d(4, 5)) == 5

    def test_distance_y(self):
        assert distance_y(Vector2d(1, -4), Vector2d(2, 7)) == 11
