from super_scad.d2.PieSlice2D4n import PieSlice2D4n
from super_scad.d3.LinearExtrude import LinearExtrude
from super_scad.scad.Context import Context
from super_scad.scad.ScadObject import ScadObject


class PieSlice3D4n(ScadObject):
    """
    Class for 3D pie slices.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self,
                 *,
                 angle: float | None = None,
                 start_angle: float | None = None,
                 end_angle: float | None = None,
                 radius: float | None = None,
                 inner_radius: float | None = None,
                 outer_radius: float | None = None,
                 height: float):
        """
        Object constructor.

        :param angle: The angle of the pie slice (implies starting angle is 0.0).
        :param start_angle: The start angle of the pie slice.
        :param end_angle: The end angle of the pie slice.
        :param radius: The radius of the pie slice (implies inner radius is 0.0).
        :param inner_radius: The inner radius of the pie slice.
        :param outer_radius: The outer radius of the pie slice.
        :param height: The height of the pie slice.
        """
        ScadObject.__init__(self, args=locals())

        self.__pie_slice2d: PieSlice2D4n = PieSlice2D4n(angle=angle,
                                                        start_angle=start_angle,
                                                        end_angle=end_angle,
                                                        radius=radius,
                                                        inner_radius=inner_radius,
                                                        outer_radius=outer_radius)
        """
        The 2D pie slice to be extruded to a 3D pie slice.
        """

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def angle(self) -> float:
        """
        Returns the angle of the pie slice.
        """
        return self.__pie_slice2d.angle

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def start_angle(self) -> float:
        """
        Returns the start angle of the pie slice.
        """
        return self.__pie_slice2d.start_angle

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def end_angle(self) -> float:
        """
        Returns the end angle of the pie slice.
        """
        return self.__pie_slice2d.end_angle

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def radius(self) -> float:
        """
        Returns the outer radius of the pie slice.
        """
        return self.__pie_slice2d.radius

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def inner_radius(self) -> float:
        """
        Returns the inner radius of the pie slice.
        """
        return self.__pie_slice2d.inner_radius

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def outer_radius(self) -> float:
        """
        Returns the outer radius of the pie slice.
        """
        return self.__pie_slice2d.outer_radius

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def height(self) -> float:
        """
        Returns the height of the pie slice.
        """
        return self.uc(self._args['height'])

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def convexity(self) -> int:
        """
        Returns the convexity of the pie slice.
        """
        return 1 if self.angle < 180.0 else 2

    # ------------------------------------------------------------------------------------------------------------------
    def build(self, context: Context) -> ScadObject:
        """
        Builds a SuperSCAD object.

        :param context: The build context.
        """
        return LinearExtrude(height=self.height, convexity=self.__pie_slice2d.convexity, child=self.__pie_slice2d)

# ----------------------------------------------------------------------------------------------------------------------
