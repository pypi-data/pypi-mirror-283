from typing import List

from super_scad.private.PrivateMultiChildScadCommand import PrivateMultiChildScadCommand
from super_scad.ScadObject import ScadObject


class Minkowski(PrivateMultiChildScadCommand):
    """
    Displays the minkowski sum of child nodes. See
    https://en.wikibooks.org/wiki/OpenSCAD_User_Manual/Transformations#minkowski.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self, *, convexity: int | None = None, children: List[ScadObject]):
        """
        Object constructor.

        :param convexity: Number of "inward" curves, i.e. expected number of path crossings of an arbitrary line through
                          the child objects.
        :param children: The child objects.
        """
        PrivateMultiChildScadCommand.__init__(self, command='minkowski', args=locals(), children=children)

# ----------------------------------------------------------------------------------------------------------------------
