from super_scad.Context import Context
from super_scad.d2.PieSlice2D import PieSlice2D
from super_scad.d3.LinearExtrude import LinearExtrude
from super_scad.ScadObject import ScadObject


class PieSlice3D(ScadObject):
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
                 height: float,
                 fa: float | None = None,
                 fs: float | None = None,
                 fn: int | None = None):
        """
        Object constructor.

        :param angle: The angle of the pie slice (implies starting angle is 0.0).
        :param start_angle: The start angle of the pie slice.
        :param end_angle: The end angle of the pie slice.
        :param radius: The radius of the pie slice (implies inner radius is 0.0).
        :param inner_radius: The inner radius of the pie slice.
        :param outer_radius: The outer radius of the pie slice.
        :param height: The height of the pie slice.
        :param fa: The minimum angle (in degrees) of each fragment.
        :param fs: The minimum circumferential length of each fragment.
        :param fn: The fixed number of fragments in 360 degrees. Values of 3 or more override fa and fs.
        """
        ScadObject.__init__(self, args=locals())

        self.__pie_slice2d: PieSlice2D = PieSlice2D(angle=angle,
                                                    start_angle=start_angle,
                                                    end_angle=end_angle,
                                                    radius=radius,
                                                    inner_radius=inner_radius,
                                                    outer_radius=outer_radius,
                                                    fa=fa,
                                                    fs=fs,
                                                    fn=fn)
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
    @property
    def fa(self) -> float | None:
        """
        Returns the minimum angle (in degrees) of each fragment.
        """
        return self.__pie_slice2d.fa

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def fs(self) -> float | None:
        """
        Returns the minimum circumferential length of each fragment.
        """
        return self.__pie_slice2d.fs

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def fn(self) -> int | None:
        """
        Returns the fixed number of fragments in 360 degrees. Values of 3 or more override $fa and $fs.
        """
        return self.__pie_slice2d.fn

    # ------------------------------------------------------------------------------------------------------------------
    def build(self, context: Context) -> ScadObject:
        """
        Builds a SuperSCAD object.

        :param context: The build context.
        """
        return LinearExtrude(height=self.height, convexity=self.__pie_slice2d.convexity, child=self.__pie_slice2d)

# ----------------------------------------------------------------------------------------------------------------------
