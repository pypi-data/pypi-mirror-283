from typing import Dict

from super_scad.private.PrivateSingleChildScadCommand import PrivateSingleChildScadCommand
from super_scad.scad.ScadObject import ScadObject
from super_scad.type.Point2 import Point2
from super_scad.type.Point3 import Point3


class PrivateScale(PrivateSingleChildScadCommand):
    """
    Scales its child objects using the specified vector. See
    https://en.wikibooks.org/wiki/OpenSCAD_User_Manual/Transformations#scale.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self, *, factor: Point2 | Point3, child: ScadObject) -> None:
        """
        Object constructor.

        :param factor: The scaling factor to apply.
        """
        PrivateSingleChildScadCommand.__init__(self, command='scale', args=locals(), child=child)

    # ------------------------------------------------------------------------------------------------------------------
    def argument_map(self) -> Dict[str, str]:
        """
        Returns the map from SuperSCAD arguments to OpenSCAD arguments.
        """
        return {'factor': 'v'}

# ----------------------------------------------------------------------------------------------------------------------
