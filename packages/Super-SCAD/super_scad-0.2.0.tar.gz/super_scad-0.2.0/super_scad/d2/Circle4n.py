import math

from super_scad.Context import Context
from super_scad.d2.Circle import Circle
from super_scad.ScadObject import ScadObject


class Circle4n(ScadObject):
    """
    Class for circle. See https://en.wikibooks.org/wiki/OpenSCAD_User_Manual/Using_the_2D_Subsystem#circle.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self, *, radius: float | None = None, diameter: float | None = None):
        """
        Object constructor.

        :param radius: The radius of the circle.
        :param diameter: The diameter of the circle.
        """
        ScadObject.__init__(self, args=locals())

    # ------------------------------------------------------------------------------------------------------------------
    def _validate_arguments(self) -> None:
        pass

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def radius(self) -> float:
        """
        Returns the radius of the circle.
        """
        return self.uc(self._args.get('radius', 0.5 * self._args.get('diameter', 0.0)))

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def diameter(self) -> float:
        """
        Returns the diameter of the circle.
        """
        return self.uc(self._args.get('diameter', 2.0 * self._args.get('radius', 0.0)))

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def r2sides(radius: float, context: Context) -> int:
        """
        Replicates the OpenSCAD logic to calculate the number of sides from the radius.

        :param radius: The radius of the circle.
        :param context: The build context.
        """
        if context.fn > 0:
            return context.fn

        return int(math.ceil(max(min(360.0 / context.fa, radius * 2.0 * math.pi / context.fs), 5.0)))

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def r2sides4n(radius: float, context: Context) -> int:
        """
        Round up the number of sides to a multiple of 4 to ensure points land on all axes.

        :param radius: The radius of the circle.
        :param context: The build context.
        """
        return int(math.floor((Circle4n.r2sides(radius, context) + 3) / 4) * 4)

    # ------------------------------------------------------------------------------------------------------------------
    def build(self, context: Context) -> ScadObject:
        """
        Builds a SuperSCAD object.

        :param context: The build context.
        """
        return Circle(diameter=self.diameter, fn=Circle4n.r2sides4n(self.radius, context))

# ----------------------------------------------------------------------------------------------------------------------
