import pytest
from pbc_by_integer import PBCByInteger, AxesTypeEnum, Vec3


class TestPBC3WithoutIfElse:
    def setup_method(self):
        self.pbc = PBCByInteger(10.0, AxesTypeEnum.NEGATIVE_POSITIVE)

    def test_wrap_negative_positive_normal_condition(self):
        loc = Vec3(3.0, -2.0, 4.0)
        wrapped = self.pbc.wrap(loc)
        assert wrapped.x == pytest.approx(loc.x)
        assert wrapped.y == pytest.approx(loc.y)
        assert wrapped.z == pytest.approx(loc.z)

    def test_wrap_negative_positive_above_half_box(self):
        loc = Vec3(6.0, 5.5, 7.0)
        wrapped = self.pbc.wrap(loc)
        assert wrapped.x == pytest.approx(-4.0)
        assert wrapped.y == pytest.approx(-4.5)
        assert wrapped.z == pytest.approx(-3.0)

    def test_wrap_negative_positive_below_half_box(self):
        loc = Vec3(-6.0, -7.0, -4.0)
        wrapped = self.pbc.wrap(loc)
        assert wrapped.x == pytest.approx(4.0)
        assert wrapped.y == pytest.approx(3.0)
        assert wrapped.z == pytest.approx(-4.0)

    def test_wrap_negative_positive_at_minus_half_box(self):
        loc = Vec3(-5.0, -5.0, -5.0)
        wrapped = self.pbc.wrap(loc)
        assert wrapped.x == pytest.approx(-5.0)
        assert wrapped.y == pytest.approx(-5.0)
        assert wrapped.z == pytest.approx(-5.0)

    def test_wrap_negative_positive_at_half_box(self):
        loc = Vec3(5.0, 5.0, 5.0)
        wrapped = self.pbc.wrap(loc)
        assert wrapped.x == pytest.approx(-5.0)
        assert wrapped.y == pytest.approx(-5.0)
        assert wrapped.z == pytest.approx(-5.0)

    def test_wrap_negative_positive_epsilon_test(self):
        loc = Vec3(4.999999999, -5.000000001, 5.000000001)
        wrapped = self.pbc.wrap(loc)
        assert wrapped.x == pytest.approx(4.999999999)
        assert wrapped.y == pytest.approx(4.999999999)
        assert wrapped.z == pytest.approx(-4.999999999)
