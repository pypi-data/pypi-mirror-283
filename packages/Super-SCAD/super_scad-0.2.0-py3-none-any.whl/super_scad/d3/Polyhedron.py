from typing import List

from super_scad.private.PrivateScadCommand import PrivateScadCommand
from super_scad.type.Face3 import Face3
from super_scad.type.Point3 import Point3


class Polyhedron(PrivateScadCommand):
    """
    Class for polyhedrons. See https://en.wikibooks.org/wiki/OpenSCAD_User_Manual/Primitive_Solids#polyhedron.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self, *, points: List[Point3], faces: List[Face3], convexity: int = 1):
        """
        Object constructor.

        :param points: See `OpenSCAD polyhedron documentation`_.
        :param faces: See `OpenSCAD polyhedron documentation`_.
        :param convexity: Number of "inward" curves, i.e. expected number of path crossings of an arbitrary line through
                          the child object.

        .. _OpenSCAD polyhedron documentation:
        https://en.wikibooks.org/wiki/OpenSCAD_User_Manual/Primitive_Solids#polyhedron
        """
        PrivateScadCommand.__init__(self, command='polyhedron', args=locals())

    # ------------------------------------------------------------------------------------------------------------------
    def _validate_arguments(self) -> None:
        pass

# ----------------------------------------------------------------------------------------------------------------------
