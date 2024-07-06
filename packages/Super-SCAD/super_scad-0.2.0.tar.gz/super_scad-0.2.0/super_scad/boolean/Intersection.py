from typing import List

from super_scad.private.PrivateMultiChildScadCommand import PrivateMultiChildScadCommand
from super_scad.ScadObject import ScadObject


class Intersection(PrivateMultiChildScadCommand):
    """
    Creates the intersection of all child nodes. This keeps the overlapping portion (logical and). See
    https://en.wikibooks.org/wiki/OpenSCAD_User_Manual/CSG_Modelling#intersection.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self, *, children: List[ScadObject]):
        """
        Object constructor.
        """
        PrivateMultiChildScadCommand.__init__(self, command='intersection', args=locals(), children=children)

# ----------------------------------------------------------------------------------------------------------------------
