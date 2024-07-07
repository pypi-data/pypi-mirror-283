from super_scad.d3.private.PrivateCube import PrivateCube
from super_scad.scad.Context import Context
from super_scad.scad.ScadObject import ScadObject
from super_scad.type.Size3 import Size3


class Cuboid(ScadObject):
    """
    Class for cuboids.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self,
                 *,
                 size: Size3 | None = None,
                 width: float | None = None,
                 depth: float | None = None,
                 height: float | None = None,
                 center: bool = False):
        """
        Object constructor.

        :param size: The size of the cuboid.
        :param width: The width (the size along the x-axis) of the cuboid.
        :param depth: The depth (the size along the y-axis) of the cuboid.
        :param height: The height (the size along the y-axis) of the cuboid.
        :param center: Whether the cuboid is centered at the origin.
        """
        ScadObject.__init__(self, args=locals())

    # ------------------------------------------------------------------------------------------------------------------
    def _validate_arguments(self) -> None:
        pass

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def center(self) -> bool:
        """
        Returns whether the cuboid is centered at the origin.
        """
        return self._args['center']

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def size(self) -> Size3:
        """
        Returns the size of the cuboid.
        """
        return Size3(width=self.width, depth=self.depth, height=self.height)

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def width(self) -> float:
        """
        Returns the width of the cuboid.
        """
        if 'size' in self._args:
            return self.uc(self._args['size'].width)

        return self.uc(self._args['width'])

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def depth(self) -> float:
        """
        Returns the depth of the cuboid.
        """
        if 'size' in self._args:
            return self.uc(self._args['size'].depth)

        return self.uc(self._args['depth'])

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def height(self) -> float:
        """
        Returns the height of the cuboid.
        """
        if 'size' in self._args:
            return self.uc(self._args['size'].height)

        return self.uc(self._args['height'])

    # ------------------------------------------------------------------------------------------------------------------
    def build(self, context: Context) -> ScadObject:
        """
        Builds a SuperSCAD object.

        :param context: The build context.
        """
        return PrivateCube(size=self.size, center=self.center)

# ----------------------------------------------------------------------------------------------------------------------
