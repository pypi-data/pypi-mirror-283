import math

from Boolean.Difference import Difference
from Context import Context
from D2.Circle4n import Circle4n
from D2.Rectangle import Rectangle
from D2.RegularPolygon import RegularPolygon
from Finished.D2.FinishedRegularPolygonFinish import FinishedRegularPolygonFinish
from ScadObject import ScadObject
from Transformation.Translate2D import Translate2D


class FinishedRegularPolygonFinishFillet(FinishedRegularPolygonFinish):
    """
    A finish for a regular polygon node (a.k.a. corner) with a fillet (i.e. rounded corner).
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self, *, radius: float):
        """
        Object constructor.

        :param radius: The radius of a node of a regular polygon.
        """
        self.__radius: float = radius
        """
        The radius of a node of a regular polygon.
        """

    # ------------------------------------------------------------------------------------------------------------------
    def finishing(self, context: Context, polygon: RegularPolygon) -> ScadObject:
        """
        Returns an SuperSCAD object that will be subtracted from a node (a.k.a. corner) of a regular polygon. It is
        assumed that the node is located at the origin and is aligned along the y-axis.
        """
        alpha = math.radians(polygon.inner_angle / 2.0)

        r = self.__radius / math.sin(alpha)
        x = self.__radius * math.cos(alpha)
        y = r * math.cos(alpha) ** 2.0

        rectangle = Translate2D(x=-x, y=-y, child=Rectangle(width=2.0 * x, depth=y + context.eps))
        circle = Translate2D(y=-r, child=Circle4n(radius=self.__radius))

        return Difference(children=[rectangle, circle])

# ----------------------------------------------------------------------------------------------------------------------
