from super_scad.Context import Context
from super_scad.ScadObject import ScadObject
from super_scad.ScadSingleChildParent import ScadSingleChildParent
from super_scad.transformation.private.PrivateScale import PrivateScale
from super_scad.type.Point3 import Point3


class Scale3D(ScadSingleChildParent):
    """
    Scales its child using a specified scaling factor.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self,
                 *,
                 factor: Point3 | float | None = None,
                 factor_x: float | None = None,
                 factor_y: float | None = None,
                 factor_z: float | None = None,
                 child: ScadObject):
        """
        Object constructor.

        :param factor: The scaling factor along all three the axes.
        :param factor_x: The scaling factor along the x-axis.
        :param factor_y: The scaling factor along the y-axis.
        :param factor_z: The scaling factor along the z-axis.
        :param child: The child of this object.
        """
        ScadSingleChildParent.__init__(self, args=locals(), child=child)

    # ------------------------------------------------------------------------------------------------------------------
    def _validate_arguments(self) -> None:
        pass

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def factor(self) -> Point3:
        """
        Returns the scaling factor along all three the axes.
        """
        return Point3(self.factor_x, self.factor_y, self.factor_z)

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
    @property
    def factor_z(self) -> float:
        """
        Returns the scaling factor along the z-axis.
        """
        if 'factor' in self._args:
            if isinstance(self._args['factor'], float):
                return self._args['factor']

            return self._args['factor'].z

        return self._args.get('factor_z', 1.0)

    # ------------------------------------------------------------------------------------------------------------------
    def build(self, context: Context) -> ScadObject:
        """
        Builds a SuperSCAD object.

        :param context: The build context.
        """
        return PrivateScale(factor=self.factor, child=self.child)

# ----------------------------------------------------------------------------------------------------------------------
