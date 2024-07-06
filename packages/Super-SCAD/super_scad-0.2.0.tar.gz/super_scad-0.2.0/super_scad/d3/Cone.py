from super_scad.Context import Context
from super_scad.d3.private.PrivateCylinder import PrivateCylinder
from super_scad.ScadObject import ScadObject


class Cone(ScadObject):
    """
    Class for cones. See https://en.wikibooks.org/wiki/OpenSCAD_User_Manual/Primitive_Solids#cylinder.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self,
                 *,
                 height: float,
                 bottom_radius: float | None = None,
                 bottom_diameter: float | None = None,
                 top_radius: float | None = None,
                 top_diameter: float | None = None,
                 center: bool = False,
                 fa: float | None = None,
                 fs: float | None = None,
                 fn: int | None = None):
        """
        Object constructor.

        :param height: The height of the cone.
        :param bottom_radius: The radius at the bottom of the cone.
        :param bottom_diameter: The diameter at the bottom of the cone.
        :param top_radius: The radius at the top of the cone.
        :param top_diameter: The diameter at the top of the cone.
        :param center: Whether the cone is centered in the z-direction.
        :param fa: The minimum angle (in degrees) of each fragment.
        :param fs: The minimum circumferential length of each fragment.
        :param fn: The fixed number of fragments in 360 degrees. Values of 3 or more override fa and fs.
        """
        ScadObject.__init__(self, args=locals())

    # ------------------------------------------------------------------------------------------------------------------
    def _validate_arguments(self) -> None:
        pass

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def center(self) -> bool:
        """
        Returns whether the cone is centered along the z-as.
        """
        return self._args['center']

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def bottom_radius(self) -> float:
        """
        Returns the bottom radius of the cone.
        """
        return self.uc(self._args.get('bottom_radius', 0.5 * self._args.get('bottom_diameter', 0.0)))

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def bottom_diameter(self) -> float:
        """
        Returns the bottom diameter of the cone.
        """
        return self.uc(self._args.get('bottom_diameter', 2.0 * self._args.get('bottom_radius', 0.0)))

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def top_radius(self) -> float:
        """
        Returns the top radius of the cone.
        """
        return self.uc(self._args.get('top_radius', 0.5 * self._args.get('top_diameter', 0.0)))

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def top_diameter(self) -> float:
        """
        Returns the top diameter of the cone.
        """
        return self.uc(self._args.get('top_diameter', 2.0 * self._args.get('top_radius', 0.0)))

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def height(self) -> float:
        """
        Returns the height of the cone.
        """
        return self.uc(self._args.get('height', 0.0))

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def fa(self) -> float | None:
        """
        Returns the minimum angle (in degrees) of each fragment.
        """
        return self._args.get('fa')

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def fs(self) -> float | None:
        """
        Returns the minimum circumferential length of each fragment.
        """
        return self.uc(self._args.get('fs'))

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def fn(self) -> int | None:
        """
        Returns the fixed number of fragments in 360 degrees. Values of 3 or more override $fa and $fs.
        """
        return self._args.get('fn')

    # ------------------------------------------------------------------------------------------------------------------
    def build(self, context: Context) -> ScadObject:
        """
        Builds a SuperSCAD object.

        :param context: The build context.
        """
        return PrivateCylinder(height=self.height,
                               bottom_diameter=self.bottom_diameter,
                               top_diameter=self.top_diameter,
                               center=self.center,
                               fa=self.fa,
                               fs=self.fs,
                               fn=self.fn)

# ----------------------------------------------------------------------------------------------------------------------
