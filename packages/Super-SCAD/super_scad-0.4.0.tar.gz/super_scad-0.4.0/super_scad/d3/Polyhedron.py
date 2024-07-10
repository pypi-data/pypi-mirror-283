from typing import List

from super_scad.private.PrivateOpenScadCommand import PrivateOpenScadCommand
from super_scad.type.Face3 import Face3
from super_scad.type.Point3 import Point3


class Polyhedron(PrivateOpenScadCommand):
    """
    Widget for creating polyhedrons. See https://en.wikibooks.org/wiki/OpenSCAD_User_Manual/Primitive_Solids#polyhedron.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self,
                 *,
                 points: List[Point3],
                 faces: List[Face3],
                 convexity: int | None = None):
        """
        Object constructor.

        :param points: Vector of 3d points or vertices. Each point is in turn a vector, [x,y,z], of its coordinates.
                       Points may be defined in any order. N points are referenced, in the order defined, as 0 to N-1.
        :param faces:  Vector of faces that collectively enclose the solid. Each face is a vector containing the
                       indices (0 based) of 3 or more points from the points vector. Faces may be defined in any order,
                       but the points of each face must be ordered correctly (see below). Define enough faces to fully
                       enclose the solid, with no overlap. If points that describe a single face are not on the same
                       plane, the face is automatically split into triangles as needed.
        :param convexity: Number of "inward" curves, i.e. expected number of path crossings of an arbitrary line through
                          the child widget.
        """
        PrivateOpenScadCommand.__init__(self, command='polyhedron', args=locals())

    # ------------------------------------------------------------------------------------------------------------------
    def _validate_arguments(self) -> None:
        pass

# ----------------------------------------------------------------------------------------------------------------------
