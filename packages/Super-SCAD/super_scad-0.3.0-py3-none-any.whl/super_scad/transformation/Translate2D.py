from super_scad.scad.Context import Context
from super_scad.scad.ScadObject import ScadObject
from super_scad.scad.ScadSingleChildParent import ScadSingleChildParent
from super_scad.transformation.private.PrivateTranslate import PrivateTranslate
from super_scad.type.Point2 import Point2


class Translate2D(ScadSingleChildParent):
    """
    Translates (moves) its child object along the specified vector. See
    https://en.wikibooks.org/wiki/OpenSCAD_User_Manual/Transformations#translate.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self,
                 *,
                 vector: Point2 | None = None,
                 x: float | None = None,
                 y: float | None = None,
                 child: ScadObject):
        """
        Object constructor.

        :param vector: The vector over which the child object is translated.
        :param x: The distance the child object is translated to along the x-axis.
        :param y: The distance the child object is translated to along the y-axis.
        :param child: The child object to be translated.
        """
        ScadSingleChildParent.__init__(self, args=locals(), child=child)

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def vector(self) -> Point2:
        """
        Returns the vector over which the child object is translated.
        """
        return Point2(self.x, self.y)

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def x(self) -> float:
        """
        Returns distance the child object is translated to along the x-axis.
        """
        if 'vector' in self._args:
            return self.uc(self._args['vector'].x)

        return self.uc(self._args.get('x', 0.0))

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def y(self) -> float:
        """
        Returns distance the child object is translated to along the y-axis.
        """
        if 'vector' in self._args:
            return self.uc(self._args['vector'].y)

        return self.uc(self._args.get('y', 0.0))

    # ------------------------------------------------------------------------------------------------------------------
    def build(self, context: Context) -> ScadObject:
        """
        Builds a SuperSCAD object.

        :param context: The build context.
        """
        return PrivateTranslate(vector=Point2(x=self.x, y=self.y), child=self.child)

# ----------------------------------------------------------------------------------------------------------------------
