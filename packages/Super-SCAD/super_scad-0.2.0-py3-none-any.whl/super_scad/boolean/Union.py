from typing import List

from super_scad.private.PrivateMultiChildScadCommand import PrivateMultiChildScadCommand
from super_scad.ScadObject import ScadObject


class Union(PrivateMultiChildScadCommand):
    """
    Creates a union of all its child nodes. This is the sum of all children (logical or). See
    https://en.wikibooks.org/wiki/OpenSCAD_User_Manual/CSG_Modelling#union.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self, *, children: List[ScadObject]):
        """
        Object constructor.
        """
        PrivateMultiChildScadCommand.__init__(self, command='union', args=locals(), children=children)

# ----------------------------------------------------------------------------------------------------------------------
