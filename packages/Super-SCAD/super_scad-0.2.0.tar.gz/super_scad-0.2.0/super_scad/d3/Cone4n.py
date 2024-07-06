from super_scad.Context import Context
from super_scad.d2.Circle4n import Circle4n
from super_scad.d3.Cone import Cone
from super_scad.ScadObject import ScadObject


class Cone4n(ScadObject):
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
                 center: bool = False):
        """
        Object constructor.

        :param height: The height of the cone.
        :param top_radius: The radius at the top of the cone.
        :param top_diameter: The diameter at the top of the cone.
        :param bottom_radius: The radius at the bottom of the cone.
        :param bottom_diameter: The diameter at the bottom of the cone.
        :param center: Whether the cone is centered in the z-direction.
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
    def build(self, context: Context) -> ScadObject:
        """
        Builds a SuperSCAD object.

        :param context: The build context.
        """
        return Cone(height=self.height,
                    bottom_diameter=self.bottom_diameter,
                    top_diameter=self.top_diameter,
                    center=self.center,
                    fn=Circle4n.r2sides4n(max(self.bottom_radius, self.top_radius), context))

# ----------------------------------------------------------------------------------------------------------------------
