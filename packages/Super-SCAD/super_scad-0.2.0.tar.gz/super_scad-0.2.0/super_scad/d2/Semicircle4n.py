from super_scad.boolean.Intersection import Intersection
from super_scad.Context import Context
from super_scad.d2.Circle4n import Circle4n
from super_scad.d2.Rectangle import Rectangle
from super_scad.ScadObject import ScadObject
from super_scad.transformation.Translate2D import Translate2D


class Semicircle4n(ScadObject):
    """
    Class for semicircles.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self, *, radius: float | None = None, diameter: float | None = None):
        """
        Object constructor.

        :param radius: See `OpenSCAD circle documentation`_.
        :param diameter: See `OpenSCAD circle documentation`_.

        .. _OpenSCAD circle documentation: https://en.wikibooks.org/wiki/OpenSCAD_User_Manual/Using_the_2D_Subsystem#circle
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
    def build(self, context: Context) -> ScadObject:
        """
        Builds a SuperSCAD object.

        :param context: The build context.
        """
        return Intersection(children=[Circle4n(diameter=self.diameter),
                                      Translate2D(x=-(self.radius + context.eps),
                                                  child=Rectangle(width=self.diameter + 2 * context.eps,
                                                                  depth=self.radius + context.eps))])

# ----------------------------------------------------------------------------------------------------------------------
