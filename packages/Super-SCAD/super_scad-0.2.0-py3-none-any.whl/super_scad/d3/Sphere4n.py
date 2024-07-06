from super_scad.Context import Context
from super_scad.d2.Circle4n import Circle4n
from super_scad.d2.Semicircle4n import Semicircle4n
from super_scad.d3.RotateExtrude import RotateExtrude
from super_scad.ScadObject import ScadObject
from super_scad.transformation.Rotate2D import Rotate2D


class Sphere4n(ScadObject):
    """
    Class for spheres. See https://en.wikibooks.org/wiki/OpenSCAD_User_Manual/Primitive_Solids#sphere.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self, *, radius: float | None = None, diameter: float | None = None):
        """
        Object constructor.

        :param radius: The radius of the sphere.
        :param diameter: The diameter of the sphere.
        """
        ScadObject.__init__(self, args=locals())

    # ------------------------------------------------------------------------------------------------------------------
    def _validate_arguments(self) -> None:
        pass

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def radius(self) -> float:
        """
        Returns the radius of the sphere.
        """
        return self.uc(self._args.get('radius', 0.5 * self._args.get('diameter', 0.0)))

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def diameter(self) -> float:
        """
        Returns the diameter of the sphere.
        """
        return self.uc(self._args.get('diameter', 2.0 * self._args.get('radius', 0.0)))

    # ------------------------------------------------------------------------------------------------------------------
    def build(self, context: Context) -> ScadObject:
        """
        Builds a SuperSCAD object.

        :param context: The build context.
        """
        return RotateExtrude(angle=360.0,
                             fn=Circle4n.r2sides4n(self.radius, context),
                             child=Rotate2D(angle=-90.0, child=Semicircle4n(diameter=self.diameter)))

# ----------------------------------------------------------------------------------------------------------------------
