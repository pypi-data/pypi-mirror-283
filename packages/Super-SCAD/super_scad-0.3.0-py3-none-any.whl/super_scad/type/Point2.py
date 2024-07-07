import math
from dataclasses import dataclass


@dataclass(frozen=True)
class Point2:
    """
    A point in 2D space.
    """
    x: float
    """
    The x-coordinate of this point.
    """

    y: float
    """
    The y-coordinate of this point.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __repr__(self):
        return f"[{self.x}, {self.y}]"

    # ------------------------------------------------------------------------------------------------------------------
    def __add__(self, other):
        return Point2(self.x + other.x, self.y + other.y)

    # ------------------------------------------------------------------------------------------------------------------
    def __sub__(self, other):
        return Point2(self.x - other.x, self.y - other.y)

    # ------------------------------------------------------------------------------------------------------------------
    def __truediv__(self, other: float):
        return Point2(self.x / other, self.y / other)

    # ------------------------------------------------------------------------------------------------------------------
    def __mul__(self, other: float):
        return Point2(self.x * other, self.y * other)

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def length(self) -> float:
        """
        Returns the length of this vector.
        """
        return math.sqrt(self.x ** 2 + self.y ** 2)

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def normal(self):
        """
        Returns the unit vector of this vector.

        :rtype: super_scad.type.Point2.Point2
        """
        length = self.length

        return Point2(self.x / length, self.y / length)

# ----------------------------------------------------------------------------------------------------------------------
