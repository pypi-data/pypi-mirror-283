from super_scad.Context import Context
from super_scad.d2.Circle4n import Circle4n
from super_scad.d3.Sphere import Sphere
from super_scad.ScadObject import ScadObject
from super_scad.transformation.Resize3D import Resize3D
from super_scad.type.Size3 import Size3


class Ellipsoid4n(ScadObject):
    """
    Class for ellipsoids.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self,
                 *,
                 radius_x: float | None = None,
                 radius_y: float | None = None,
                 radius_z: float | None = None,
                 diameter_x: float | None = None,
                 diameter_y: float | None = None,
                 diameter_z: float | None = None):
        """
        Object constructor.

        :param radius_x: The radius of the ellipsoid in x-direction.
        :param radius_y: The radius of the ellipsoid in y-direction.
        :param radius_z: The radius of the ellipsoid in z-direction.
        :param diameter_x: The diameter of the ellipsoid in x-direction.
        :param diameter_y: The diameter of the ellipsoid in y-direction.
        :param diameter_z: The diameter of the ellipsoid in z-direction.
        """
        ScadObject.__init__(self, args=locals())

    # ------------------------------------------------------------------------------------------------------------------
    def _validate_arguments(self) -> None:
        pass

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def radius_x(self) -> float:
        """
        Returns the radius of the ellipsoid in x-direction.
        """
        return self.uc(self._args.get('radius_x', 0.5 * self._args.get('diameter_x', 0.0)))

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def radius_y(self) -> float:
        """
        Returns the radius of the ellipsoid in y-direction.
        """
        return self.uc(self._args.get('radius_y', 0.5 * self._args.get('diameter_y', 0.0)))

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def radius_z(self) -> float:
        """
        Returns the radius of the ellipsoid in z-direction.
        """
        return self.uc(self._args.get('radius_z', 0.5 * self._args.get('diameter_z', 0.0)))

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def diameter_x(self) -> float:
        """
        Returns the length of the ellipsoid in x-direction.
        """
        return self.uc(self._args.get('diameter_x', 2.0 * self._args.get('radius_x', 0.0)))

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def diameter_y(self) -> float:
        """
        Returns the length of the ellipsoid in y-direction.
        """
        return self.uc(self._args.get('diameter_y', 2.0 * self._args.get('radius_y', 0.0)))

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def diameter_z(self) -> float:
        """
        Returns the length of the ellipsoid in z-direction.
        """
        return self.uc(self._args.get('diameter_z', 2.0 * self._args.get('radius_z', 0.0)))

    # ------------------------------------------------------------------------------------------------------------------
    def build(self, context: Context) -> ScadObject:
        """
        Builds a SuperSCAD object.

        :param context: The build context.
        """
        diameter: float = max(self.diameter_x, self.diameter_y, self.diameter_z)

        return Resize3D(new_size=Size3(self.diameter_x, self.diameter_y, self.diameter_z),
                        child=Sphere(diameter=diameter, fn=Circle4n.r2sides4n(0.5 * diameter, context)))

# ----------------------------------------------------------------------------------------------------------------------
