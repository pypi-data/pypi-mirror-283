from enum import Enum


class Unit(Enum):
    """
    Enumeration of all possible units of lengths.
    """

    FREE = 0
    """
    Free of any scale.
    """

    MM = 1
    """
    Millimeters (metric).
    """

    INCH = 2
    """
    Inches (imperial).
    """
