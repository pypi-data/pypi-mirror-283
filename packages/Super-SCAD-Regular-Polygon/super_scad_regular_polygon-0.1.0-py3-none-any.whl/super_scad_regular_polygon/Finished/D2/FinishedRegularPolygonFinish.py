from Context import Context
from D2.RegularPolygon import RegularPolygon
from ScadObject import ScadObject


class FinishedRegularPolygonFinish:
    """
    Interface for finishing the nodes (a.k.a. corners) of a regular polygon.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def finishing(self, context: Context, polygon: RegularPolygon) -> ScadObject:
        """
        Returns an SuperSCAD object that will be subtracted from a node (a.k.a. corner) of a regular polygon. It is
        assumed that the node is located at the origin and is aligned along the y-axis.
        """
        raise NotImplementedError()

# ----------------------------------------------------------------------------------------------------------------------
