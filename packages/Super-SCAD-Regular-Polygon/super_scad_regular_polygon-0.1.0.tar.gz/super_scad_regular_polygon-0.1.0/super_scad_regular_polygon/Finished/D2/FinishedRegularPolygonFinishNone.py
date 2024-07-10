from Boolean.Union import Union
from Context import Context
from D2.RegularPolygon import RegularPolygon
from Finished.D2.FinishedRegularPolygonFinish import FinishedRegularPolygonFinish
from ScadObject import ScadObject


class FinishedRegularPolygonFinishNone(FinishedRegularPolygonFinish):
    """
    A finish for a regular polygon node that does not remove anything.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def finishing(self, context: Context, polygon: RegularPolygon) -> ScadObject:
        """
        Returns an SuperSCAD object that will be subtracted from a node (a.k.a. corner) of a regular polygon. It is
        assumed that the node is located at the origin and is aligned along the y-axis.
        """
        return Union(children=[])

# ----------------------------------------------------------------------------------------------------------------------
