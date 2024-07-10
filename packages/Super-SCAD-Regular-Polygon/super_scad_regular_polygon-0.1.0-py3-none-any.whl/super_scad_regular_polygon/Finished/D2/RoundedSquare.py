from Context import Context
from D2.RegularPolygon import RegularPolygon
from Finished.D2.FinishedRegularPolygon import FinishedRegularPolygon
from Finished.D2.FinishedRegularPolygonFinishFillet import FinishedRegularPolygonFinishFillet
from ScadObject import ScadObject
from Transformation.Translate2D import Translate2D


class RoundedSquare(ScadObject):
    """
    Class for squares with rounded corners.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self, *, size: float, radius: float, center: bool = False):
        """
        Object constructor.

        :param size: The length of the edges of the (rounded) square.
        :param radius: The radius of the rounded square.
        """
        ScadObject.__init__(self, args=locals())

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def center(self) -> bool:
        """
        Returns whether the rounded square is centered at (0,0).
        """
        return self._args['center']

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def radius(self) -> float:
        """
        Returns the radius of the rounded corners.
        """
        return self._args['radius']

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def size(self) -> float:
        """
        Returns the length of the edges of the (rounded) square.
        """
        return self._args['size']

    # ------------------------------------------------------------------------------------------------------------------
    def build(self, context: Context) -> ScadObject:
        """
        Builds a SuperSCAD object.

        :param context: The build context.

        :rtype: ScadObject
        """
        rounded_square = FinishedRegularPolygon(finish=FinishedRegularPolygonFinishFillet(radius=self.radius),
                                                child=RegularPolygon(size=self.size, sides=4))

        if not self.center:
            rounded_square = Translate2D(x=self.size / 2.0, y=self.size / 2.0, child=rounded_square)

        return rounded_square

# ----------------------------------------------------------------------------------------------------------------------
