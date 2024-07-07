from super_scad.scad.Context import Context
from super_scad.scad.ScadObject import ScadObject
from super_scad.scad.ScadSingleChildParent import ScadSingleChildParent
from super_scad.transformation.private.PrivateRotate import PrivateRotate
from super_scad.type.Point2 import Point2


class Flip2D(ScadSingleChildParent):
    """
    Flips its child about the x or y-axis.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self,
                 *,
                 horizontal: bool | None = None,
                 vertical: bool | None = None,
                 flip_x: bool = False,
                 flip_y: bool = False,
                 child: ScadObject) -> None:
        """
        Object constructor.

        :param horizontal: Whether to flip the child object horizontally (i.e. flip around the y-axis).
        :param vertical: Whether to flip the child object vertically (i.e. flip around the x-axis).
        :param flip_x: Whether to flip the child object around the x-asis (i.e. vertical flip).
        :param flip_y: Whether to flip the child object around the y-asis (i.e. horizontal flip).
        :param child: The child object to be flipped.
        """
        ScadSingleChildParent.__init__(self, args=locals(), child=child)

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def horizontal(self) -> bool:
        """
        Returns whether to flip the child object horizontally (i.e. flip around the y-axis).
        """
        return self._args.get('horizontal', False) or self._args.get('flip_y', False)

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def vertical(self) -> bool:
        """
        Returns whether to flip the child object vertically (i.e. flip around the x-axis).
        """
        return self._args.get('vertical', False) or self._args.get('flip_x', False)

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def flip_x(self) -> bool:
        """
        Returns whether to flip the child object around the x-asis (i.e. vertical flip).
        """
        return self.vertical

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def flip_y(self) -> bool:
        """
        Returns whether to flip the child object around the y-asis (i.e. horizontal flip).
        """
        return self.horizontal

    # ------------------------------------------------------------------------------------------------------------------
    def build(self, context: Context) -> ScadObject:
        """
        Builds a SuperSCAD object.

        :param context: The build context.
        """
        angle = Point2(x=180.0 if self.flip_x else 0.0, y=180.0 if self.flip_y else 0.0)

        return PrivateRotate(angle=angle, child=self.child)

# ----------------------------------------------------------------------------------------------------------------------
