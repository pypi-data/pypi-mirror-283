from typing import List

from Boolean.Difference import Difference
from Context import Context
from D2.RegularPolygon import RegularPolygon
from Finished.D2.FinishedRegularPolygonFinish import FinishedRegularPolygonFinish
from ScadObject import ScadObject
from ScadSingleChildParent import ScadSingleChildParent
from Transformation.Rotate2D import Rotate2D
from Transformation.Translate2D import Translate2D


class FinishedRegularPolygon(ScadSingleChildParent):
    """
    Class for regular polygons.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self, *, child: RegularPolygon,
                 finish: FinishedRegularPolygonFinish | List[FinishedRegularPolygonFinish]):
        """
        Object constructor.
        """
        ScadSingleChildParent.__init__(self, locals(), child)

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def finishing(self) -> List[FinishedRegularPolygonFinish]:
        """

        :return:
        """
        child = self.child
        if isinstance(child, RegularPolygon):
            finishing = self._args['finish']
            if isinstance(finishing, FinishedRegularPolygonFinish):
                ret = []
                for i in range(0, child.sides):
                    ret.append(finishing)

                return ret

            if isinstance(finishing, List):
                ret = []
                n = len(finishing)
                for i in range(0, child.sides):
                    ret.append(finishing[i % n])

                return ret

        return []

    # ------------------------------------------------------------------------------------------------------------------
    def build(self, context: Context) -> ScadObject:
        """
        Builds a SuperSCAD object.

        :param context: The build context.

        :rtype: ScadObject
        """
        child = self.child
        children = [child]

        if isinstance(child, RegularPolygon):
            angles = child.angles
            points = child.points
            finishing = self.finishing

            for i in range(0, len(angles)):
                children.append(Translate2D(x=points[i].x,
                                            y=points[i].y,
                                            child=Rotate2D(angle=angles[i] - 90.0,
                                                           child=finishing[i].finishing(context, child))))

        return Difference(children=children)

# ----------------------------------------------------------------------------------------------------------------------
