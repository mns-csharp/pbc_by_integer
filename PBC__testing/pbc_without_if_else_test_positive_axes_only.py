import math
import pytest

from pbc_without_if_else import PBC3WithoutIfElse, AxesTypeEnum, Vec3


class TestPBC3WithoutIfElse:
    def setup_method(self):
        self.pbc_positive = PBC3WithoutIfElse(10, AxesTypeEnum.POSITIVE)

    def test_wrap_positive(self):
        assert self.pbc_positive.wrap_positive(10, 12) == 2
        assert self.pbc_positive.wrap_positive(10, -3) == 7

    def test_wrap(self):
        wrapped = self.pbc_positive.wrap(Vec3(12, -3, 15))
        assert wrapped.x == 2
        assert wrapped.y == 7
        assert wrapped.z == 5

    def test_distance_sqr(self):
        p1 = Vec3(1, 1, 1)
        p2 = Vec3(9, 9, 9)
        assert math.isclose(self.pbc_positive.distance_sqr(p1, p2), 6 ** 2 + 6 ** 2 + 6 ** 2)

    def test_distance(self):
        p1 = Vec3(1, 1, 1)
        p2 = Vec3(9, 9, 9)
        assert math.isclose(self.pbc_positive.distance(p1, p2), math.sqrt(6 ** 2 + 6 ** 2 + 6 ** 2))
