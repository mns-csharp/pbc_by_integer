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


class PBCByInteger:
    """
    Implements periodic boundary conditions for a cubic simulation box.
    This class efficiently calculates distances and wraps particle coordinates
    using a scaled integer representation for enhanced performance.
    """

    def __init__(self, box_length, axes_type=AxesTypeEnum.POSITIVE):
        """
        Initializes a new instance of the PBCByInteger class.

        :param box_length: The physical length of the simulation box.
        :param axes_type: The type of periodic boundary condition to apply.
        """
        self.box_size = (2 ** 63) // 2  # Equivalent to long.MaxValue / 2
        self.half_box_size = self.box_size // 2
        self.scale_factor = self.box_size / box_length
        self.periodic_distance = box_length
        self._axes_type = None
        self._wrap_function = None
        self.axes_type = axes_type  # Setter will initialize the wrap function
        self.disposed = False

    @property
    def axes_type(self):
        return self._axes_type

    @axes_type.setter
    def axes_type(self, value):
        self._axes_type = value
        mapping = {
            AxesTypeEnum.POSITIVE: self._wrap_positive,
            AxesTypeEnum.NEGATIVE_POSITIVE: self._wrap_negative_positive
        }
        self._wrap_function = mapping.get(value)
        if self._wrap_function is None:
            raise ValueError(f"Unsupported AxesTypeEnum: {value}")

    def _to_scaled(self, position):
        return int(position * self.scale_factor)

    def _to_unscaled(self, position):
        return position / self.scale_factor

    def _wrap_positive(self, position):
        scaled_pos = self._to_scaled(position)
        return self._to_unscaled((scaled_pos % self.box_size + self.box_size) % self.box_size)

    def _wrap_negative_positive(self, position):
        half_distance = self.periodic_distance / 2.0
        scaled_pos = self._to_scaled(position + half_distance)
        wrapped = ((scaled_pos % self.box_size + self.box_size) % self.box_size) - self.box_size // 2
        return self._to_unscaled(wrapped)

    def wrap(self, loc):
        return Vec3(
            self._wrap_function(loc.x),
            self._wrap_function(loc.y),
            self._wrap_function(loc.z)
        )

    def apply_mic(self, delta):
        scaled_delta = self._to_scaled(delta)
        return self._to_unscaled(scaled_delta - self.box_size * round(scaled_delta / self.box_size))

    def distance_sqr(self, point1, point2):
        delta_x = self.apply_mic(point2.x - point1.x)
        delta_y = self.apply_mic(point2.y - point1.y)
        delta_z = self.apply_mic(point2.z - point1.z)
        return delta_x ** 2 + delta_y ** 2 + delta_z ** 2

    def distance(self, point1, point2):
        return math.sqrt(self.distance_sqr(point1, point2))


