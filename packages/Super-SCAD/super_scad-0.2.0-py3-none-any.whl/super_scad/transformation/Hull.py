from typing import List

from super_scad.private.PrivateMultiChildScadCommand import PrivateMultiChildScadCommand
from super_scad.ScadObject import ScadObject


class Hull(PrivateMultiChildScadCommand):
    """
    Displays the convex hull of child nodes. See
    https://en.wikibooks.org/wiki/OpenSCAD_User_Manual/Transformations#hull.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self, children: List[ScadObject]):
        """
        Object constructor.
        """
        PrivateMultiChildScadCommand.__init__(self, command='hull', args=locals(), children=children)

# ----------------------------------------------------------------------------------------------------------------------
