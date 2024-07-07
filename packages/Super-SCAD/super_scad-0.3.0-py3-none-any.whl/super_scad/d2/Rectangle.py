from super_scad.d2.private.PrivateSquare import PrivateSquare
from super_scad.scad.Context import Context
from super_scad.scad.ScadObject import ScadObject
from super_scad.type.Size2 import Size2


class Rectangle(ScadObject):
    """
    Class for rectangles.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self,
                 *,
                 size: Size2 | None = None,
                 width: float | None = None,
                 depth: float | None = None,
                 center: bool = False):
        """
        Object constructor.

        :param size: The size of the rectangle.
        :param width: The width (the size along the x-axis) of the rectangle.
        :param depth: The depth (the size along the y-axis) of the rectangle.
        :param center: Whether the rectangle is centered at the origin.
        """
        ScadObject.__init__(self, args=locals())

    # ------------------------------------------------------------------------------------------------------------------
    def _validate_arguments(self) -> None:
        pass

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def size(self) -> Size2:
        """
        Returns the size of the rectangle.
        """
        return Size2(width=self.width, depth=self.depth)

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def width(self) -> float:
        """
        Returns the width (the size along the x-axis) of the rectangle.
        """
        if 'size' in self._args:
            return self.uc(self._args['size'].width)

        return self.uc(self._args['width'])

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def depth(self) -> float:
        """
        Returns the depth (the size along the y-axis) of the rectangle.
        """
        if 'size' in self._args:
            return self.uc(self._args['size'].depth)

        return self.uc(self._args['depth'])

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def center(self) -> bool:
        """
        Returns whether the rectangle is centered at the origin.
        """
        return self._args['center']

    # ------------------------------------------------------------------------------------------------------------------
    def build(self, context: Context) -> ScadObject:
        """
        Builds a SuperSCAD object.

        :param context: The build context.
        """
        return PrivateSquare(size=self.size, center=self.center)

# ----------------------------------------------------------------------------------------------------------------------
