from abc import ABC
from typing import Any, Dict

from super_scad.scad.ScadObject import ScadObject


class ScadSingleChildParent(ScadObject, ABC):
    """
    Abstract parent class for SuperSCAD objects that have a single-child.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self, args: Dict[str, Any], child: ScadObject):
        """
        Object constructor.

        :param child: The child SuperSCAD object of this single-child parent.
        """
        ScadObject.__init__(self, args=args)

        self.__child = child
        """
        The child SuperSCAD object of this single-child parent.
        """

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def child(self) -> ScadObject:
        """
        Returns the child of this single-child parent.
        """
        return self.__child

# ----------------------------------------------------------------------------------------------------------------------
