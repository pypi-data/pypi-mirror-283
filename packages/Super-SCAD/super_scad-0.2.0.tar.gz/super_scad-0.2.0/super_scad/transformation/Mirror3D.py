from super_scad.Context import Context
from super_scad.ScadObject import ScadObject
from super_scad.ScadSingleChildParent import ScadSingleChildParent
from super_scad.transformation.private.PrivateMirror import PrivateMirror
from super_scad.type.Point3 import Point3


class Mirror3D(ScadSingleChildParent):
    """
    Transforms the child object to a mirror of the original, as if it were the mirror image seen through a plane
    intersecting the origin. See https://en.wikibooks.org/wiki/OpenSCAD_User_Manual/Transformations#mirror.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self,
                 *,
                 vector: Point3 | None = None,
                 x: float | None = None,
                 y: float | None = None,
                 z: float | None = None,
                 child: ScadObject):
        """
        Object constructor.

        :param vector:  The normal vector of the origin-intersecting mirror plane used, meaning the vector coming
                        perpendicularly out of the plane. Each coordinate of the original object is altered such that
                        it becomes equidistant on the other side of this plane from the closest point on the plane.
        :param x:  The x-coordinate of the origin-intersecting mirror plane.
        :param y:  The y-coordinate of the origin-intersecting mirror plane.
        """
        ScadSingleChildParent.__init__(self, args=locals(), child=child)

        self.__vector: Point3 | None = None
        """
        The normalized normal vector of the origin-intersecting mirror plane used.
        """

    # ------------------------------------------------------------------------------------------------------------------
    def _validate_arguments(self) -> None:
        pass

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def vector(self) -> Point3:
        """
        The normal vector of the origin-intersecting mirror plane.
        """
        if self.__vector is None:
            if 'vector' in self._args:
                self.__vector = self.uc(self._args['vector']).normal

            if 'x' in self._args or 'y' in self._args or 'z' in self._args:
                self.__vector = self.uc(Point3(self._args.get('x', 0.0),
                                               self._args.get('y', 0.0),
                                               self._args.get('z', 0.0))).normal

            self.__vector = self.__vector * (-1.0 if self.__vector.x < 0.0 else 1.0)

        return self.__vector

    # ------------------------------------------------------------------------------------------------------------------
    def build(self, context: Context) -> ScadObject:
        """
        Builds a SuperSCAD object.

        :param context: The build context.
        """
        return PrivateMirror(vector=self.vector, child=self.child)

# ----------------------------------------------------------------------------------------------------------------------
