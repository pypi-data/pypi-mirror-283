from typing import Any, Dict, List

from super_scad.private.PrivateScadCommand import PrivateScadCommand
from super_scad.ScadMultiChildParent import ScadMultiChildParent
from super_scad.ScadObject import ScadObject


class PrivateMultiChildScadCommand(PrivateScadCommand, ScadMultiChildParent):
    """
    Parent class for OpenSCAD commands with a multiple children.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self, command: str, args: Dict[str, Any], children: List[ScadObject]):
        """
        Object constructor.

        :param command: The OpenSCAD command.
        :param args: The arguments of the command.
        :param children: The child SuperSCAD objects of this multi-child parent.
        """
        PrivateScadCommand.__init__(self, command=command, args=args)
        ScadMultiChildParent.__init__(self, args=args, children=children)

    # ------------------------------------------------------------------------------------------------------------------
    def children(self):
        """
        Returns the children of this multi-child command.

        :rtype: List[ScadObject]|ScadObject|None
        """
        return ScadMultiChildParent.children(self)

# ----------------------------------------------------------------------------------------------------------------------
