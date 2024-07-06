from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class Face3:
    """
    A face in 3D space.
    """
    points: List[int]
    """
    The points of the face.
    """

# ----------------------------------------------------------------------------------------------------------------------
