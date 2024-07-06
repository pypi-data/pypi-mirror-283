from super_scad.private.PrivateSingleChildScadCommand import PrivateSingleChildScadCommand
from super_scad.ScadObject import ScadObject


class PrivateProjection(PrivateSingleChildScadCommand):

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self, *, cut: bool, child: ScadObject) -> None:
        """
        Object constructor.

        :param cut: Whether to cut the 3D model at height 0.0.
        :param child: The child object.
        """
        PrivateSingleChildScadCommand.__init__(self, command='projection', args=locals(), child=child)

# ----------------------------------------------------------------------------------------------------------------------
