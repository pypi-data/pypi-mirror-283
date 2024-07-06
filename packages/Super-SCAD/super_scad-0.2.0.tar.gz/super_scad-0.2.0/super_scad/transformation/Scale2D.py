from super_scad.Context import Context
from super_scad.ScadObject import ScadObject
from super_scad.ScadSingleChildParent import ScadSingleChildParent
from super_scad.transformation.private.PrivateScale import PrivateScale
from super_scad.type.Point2 import Point2


class Scale2D(ScadSingleChildParent):
    """
    Scales its child using a specified scaling factor.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self,
                 *,
                 factor: Point2 | float | None = None,
                 factor_x: float | None = None,
                 factor_y: float | None = None,
                 child: ScadObject):
        """
        Object constructor.

        :param factor: The scaling factor along all two the axes.
        :param factor_x: The scaling factor along the x-axis.
        :param factor_y: The scaling factor along the y-axis.
        :param child: The child of this object.
        """
        ScadSingleChildParent.__init__(self, args=locals(), child=child)

    # ------------------------------------------------------------------------------------------------------------------
    def _validate_arguments(self) -> None:
        pass

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def factor(self) -> Point2:
        """
        Returns the scaling factor along all two axes.
        """
        return Point2(self.factor_x, self.factor_y)

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def factor_x(self) -> float:
        """
        Returns the scaling factor along the x-axis.
        """
        if 'factor' in self._args:
            if isinstance(self._args['factor'], float):
                return self._args['factor']

            return self._args['factor'].x

        return self._args.get('factor_x', 1.0)

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def factor_y(self) -> float:
        """
        Returns the scaling factor along the y-axis.
        """
        if 'factor' in self._args:
            if isinstance(self._args['factor'], float):
                return self._args['factor']

            return self._args['factor'].y

        return self._args.get('factor_y', 1.0)

    # ------------------------------------------------------------------------------------------------------------------
    def build(self, context: Context) -> ScadObject:
        """
        Builds a SuperSCAD object.

        :param context: The build context.
        """
        return PrivateScale(factor=self.factor, child=self.child)

# ----------------------------------------------------------------------------------------------------------------------
