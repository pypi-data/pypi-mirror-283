from typing import Dict, Set

from super_scad.private.PrivateSingleChildScadCommand import PrivateSingleChildScadCommand
from super_scad.ScadObject import ScadObject


class Offset(PrivateSingleChildScadCommand):
    """
    Offset generates a new 2d interior or exterior outline from an existing outline. See
    https://en.wikibooks.org/wiki/OpenSCAD_User_Manual/Transformations#offset.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self,
                 *,
                 radius: float | None = None,
                 delta: float | None = None,
                 chamfer: bool | None = None,
                 fa: float | None = None,
                 fs: float | None = None,
                 fn: int | None = None,
                 child: ScadObject):
        """
        Object constructor.

        :param radius: The radius of the circle that is rotated about the outline, either inside or outside. This mode
                       produces rounded corners.
        :param delta: The distance of the new outline from the original outline, and therefore reproduces angled
                      corners. No inward perimeter is generated in places where the perimeter would cross itself.
        :param chamfer: When using the delta parameter, this flag defines if edges should be chamfered (cut off with a
                        straight line) or not (extended to their intersection). This parameter has no effect on radial
                        offsets.
        :param child: The child object.
        """
        if delta is not None:
            if chamfer is None:
                chamfer = False
        else:
            chamfer = None

        PrivateSingleChildScadCommand.__init__(self, command='offset', args=locals(), child=child)

    # ------------------------------------------------------------------------------------------------------------------
    def argument_map(self) -> Dict[str, str]:
        """
        Returns the map from SuperSCAD arguments to OpenSCAD arguments.
        """
        return {'radius': 'r', 'fa': '$fa', 'fs': '$fs', 'fn': '$fn'}

    # ------------------------------------------------------------------------------------------------------------------
    def argument_lengths(self) -> Set[str]:
        """
        Returns the set with arguments that are lengths.
        """
        return {'r', 'delta', '$fs'}

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def radius(self) -> float | None:
        """
        Returns the radius.
        """
        return self.uc(self._args.get('radius'))

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def delta(self) -> float | None:
        """
        Returns the delta.
        """
        return self.uc(self._args.get('delta'))

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def chamfer(self) -> bool | None:
        """
        Returns the delta.
        """
        return self._args.get('chamfer')

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def fa(self) -> float | None:
        """
        Returns the minimum angle (in degrees) of each fragment.
        """
        return self._args.get('fa')

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def fs(self) -> float | None:
        """
        Returns the minimum circumferential length of each fragment.
        """
        return self.uc(self._args.get('fs'))

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def fn(self) -> int | None:
        """
        Returns the fixed number of fragments in 360 degrees. Values of 3 or more override $fa and $fs.
        """
        return self._args.get('fn')

# ----------------------------------------------------------------------------------------------------------------------
