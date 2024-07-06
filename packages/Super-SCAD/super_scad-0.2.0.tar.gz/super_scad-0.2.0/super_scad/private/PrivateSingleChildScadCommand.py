from typing import Any, Dict

from super_scad.private.PrivateScadCommand import PrivateScadCommand
from super_scad.ScadObject import ScadObject
from super_scad.ScadSingleChildParent import ScadSingleChildParent


class PrivateSingleChildScadCommand(PrivateScadCommand, ScadSingleChildParent):
    """
    Parent class for OpenSCAD commands with a single child.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self, command: str, args: Dict[str, Any], child: ScadObject):
        """
        Object constructor.

        :param command: The OpenSCAD command.
        :param args: The arguments of the command.
        :param child: The child SuperSCAD object of this single-child parent.
        """
        PrivateScadCommand.__init__(self, command=command, args=args)
        ScadSingleChildParent.__init__(self, args=args, child=child)

    # ------------------------------------------------------------------------------------------------------------------
    def children(self):
        """
        Returns the child of this single-child command.

        :rtype: List[ScadObject]|ScadObject|None
        """
        return ScadSingleChildParent.children(self)

# ----------------------------------------------------------------------------------------------------------------------
