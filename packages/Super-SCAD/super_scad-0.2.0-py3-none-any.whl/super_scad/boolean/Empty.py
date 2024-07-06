from super_scad.boolean.Union import Union
from super_scad.Context import Context
from super_scad.ScadObject import ScadObject


class Empty(ScadObject):
    """
    Create an empty OpenSCAD object.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def build(self, context: Context) -> ScadObject:
        """
        Builds a SuperSCAD object.

        :param context: The build context.
        """
        return Union(children=[])

# ----------------------------------------------------------------------------------------------------------------------
