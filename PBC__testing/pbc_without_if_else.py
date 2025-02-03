import math
from enum import Enum


class AxesTypeEnum(Enum):
    POSITIVE = 1
    NEGATIVE_POSITIVE = 2


class Vec3:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __repr__(self):
        return f"Vec3({self.x}, {self.y}, {self.z})"


class PBC3WithoutIfElse:
    def __init__(self, periodic_length=None, axes_type=None):
        self._function = None
        self._periodic_distance = None
        self._axes_type = None

        if periodic_length is not None:
            self.periodic_distance = periodic_length

        if axes_type is not None:
            self.axes_type = axes_type

    @property
    def periodic_distance(self):
        if self._periodic_distance is None:
            raise ValueError("PeriodicDistance not set.")
        return self._periodic_distance

    @periodic_distance.setter
    def periodic_distance(self, value):
        self._periodic_distance = value

    @property
    def axes_type(self):
        if self._axes_type is None:
            raise ValueError("AxesTypeEnum is not set.")
        return self._axes_type

    @axes_type.setter
    def axes_type(self, value):
        self._axes_type = value
        mapping = {
            AxesTypeEnum.POSITIVE: self.wrap_positive,
            AxesTypeEnum.NEGATIVE_POSITIVE: self.wrap_negative_positive
        }
        self._function = mapping.get(value)
        if self._function is None:
            raise ValueError(f"Unsupported AxesTypeEnum: {value}")

    def wrap(self, loc):
        if self._function is None:
            raise ValueError("Wrapping function is not initialized.")

        periodic_length = self.periodic_distance
        x = self._function(periodic_length, loc.x)
        y = self._function(periodic_length, loc.y)
        z = self._function(periodic_length, loc.z)

        return Vec3(x, y, z)

    @staticmethod
    def wrap_positive(periodic_distance, position):
        return (position % periodic_distance + periodic_distance) % periodic_distance

    @staticmethod
    def wrap_negative_positive(periodic_distance, position):
        half_distance = periodic_distance / 2.0
        wrapped = ((
                               position + half_distance) % periodic_distance + periodic_distance) % periodic_distance - half_distance
        return wrapped

    def distance_sqr(self, point1, point2):
        delta_x = self.apply_mic(point2.x - point1.x)
        delta_y = self.apply_mic(point2.y - point1.y)
        delta_z = self.apply_mic(point2.z - point1.z)
        return delta_x ** 2 + delta_y ** 2 + delta_z ** 2

    def distance(self, point1, point2):
        return math.sqrt(self.distance_sqr(point1, point2))

    def apply_mic(self, delta):
        half_box_length = self.periodic_distance / 2.0
        return delta - self.periodic_distance * round(delta / self.periodic_distance)

    def __del__(self):
        pass
