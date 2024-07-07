from pathlib import Path
from typing import Dict

from super_scad.private.PrivateScadCommand import PrivateScadCommand
from super_scad.scad.Context import Context
from super_scad.scad.ScadObject import ScadObject


class Surface(PrivateScadCommand):
    """
    Surface reads Heightmap information from text or image files. See
    https://en.wikibooks.org/wiki/OpenSCAD_User_Manual/Other_Language_Features#surface.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self,
                 *,
                 path: str | Path,
                 center: bool = False,
                 invert: bool | None = None,
                 convexity: int | None = None):
        """
        Object constructor.

        :param path: The path to the file containing the heightmap data.
        :param center: Whether the object is centered in X- and Y-axis. Otherwise, the object is placed in the positive
                       quadrant.
        :param invert: Whether to invert how the color values of imported images are translated into height values. This
                       has no effect when importing text data files.
        :param convexity: Number of "inward" curves, i.e. expected number of path crossings of an arbitrary line through
                          the child object.
        """
        if path is not None:
            path = str(path)

        PrivateScadCommand.__init__(self, command='surface', args=locals())

    # ------------------------------------------------------------------------------------------------------------------
    def _validate_arguments(self) -> None:
        pass

    # ------------------------------------------------------------------------------------------------------------------
    def argument_map(self) -> Dict[str, str]:
        """
        Returns the map from SuperSCAD arguments to OpenSCAD arguments.
        """
        return {'path': 'file'}

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def convexity(self) -> int | None:
        """
        Returns the number of "inward" curves, i.e. expected number of path crossings of an arbitrary line through the
        child object.
        """
        return self._args.get('convexity')

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def invert(self) -> bool:
        """
        Returns whether to invert how the color values of imported images are translated into height values. This
        has no effect when importing text data files.
        """
        return self._args['invert']

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def center(self) -> bool:
        """
        Returns whether the object is centered in X- and Y-axis. Otherwise, the object is placed in the positive
        quadrant.
        """
        return self._args['center']

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def path(self) -> Path:
        """
        Returns The absolute path or the relative path from the target script to the file that will be imported.
        """
        return Path(self._args['path'])

    # ------------------------------------------------------------------------------------------------------------------
    def build(self, context: Context) -> ScadObject:
        """
        Builds a SuperSCAD object.

        :param context: The build context.
        """
        path = self.path
        if not path.is_absolute():
            path = context.target_path.parent.joinpath(path)

        if not path.is_file():
            raise FileNotFoundError(f'File {path} does not exist.')

        return self

# ----------------------------------------------------------------------------------------------------------------------
