import math
from typing import Tuple

from Context import Context
from D2.Rectangle import Rectangle
from D2.RegularPolygon import RegularPolygon
from Finished.D2.FinishedRegularPolygonFinish import FinishedRegularPolygonFinish
from ScadObject import ScadObject
from Transformation.Rotate2D import Rotate2D
from Transformation.Translate2D import Translate2D
from Type.Point2 import Point2


class FinishedRegularPolygonFinishChamfer(FinishedRegularPolygonFinish):
    """
    A finish for a regular polygon node (a.k.a. corner) with a chamfer (i.e. straight edge between two edges).
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self,
                 *,
                 length: float | None = None,
                 height: float | None = None,
                 left_length: float | None = None,
                 right_length: float | None = None,
                 angle: float | None = None):
        """
        Object constructor.

        :param length: The length of the chamfer.
        :param height: The height of the chamfer.
        :param left_length: The length of the material removed from the left edge of the regular polygon.
        :param right_length: The length of the material removed from the right edge of the regular polygon.
        :param angle: The angle relative tot the left edge of the regular polygon or the chamfer.
        """
        self.__length: float | None = length
        """
        The length of the chamfer.
        """

        self.__height: float | None = height
        """
        The height of the chamfer.
        """

        self.__left_length: float | None = left_length
        """
        The length of the material removed from the left edge of the regular polygon.
        """

        self.__right_length: float | None = right_length
        """
        The length of the material removed from the right edge of the regular polygon.
        """

        self.__angle: float | None = angle
        """
        The angle relative to the left edge of the regular polygon or the chamfer.
        """

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def __points_from_length_and_angle(length: float, angle: float, polygon: RegularPolygon) -> Tuple[Point2, Point2]:
        """
        Returns the intersection points of the chamfer and the two edges of the regular polygon given the length and
        the angle of the chamfer.

        :param length: The length of the chamfer.
        :param angle: The angle relative to the left edge of the regular polygon or the chamfer.
        :param polygon: The regular polygon.
        """
        angle_left = angle
        angle_right = math.pi - math.radians(polygon.inner_angle) - angle_left

        length_left = length / (
                math.cos(angle_left) + math.sin(angle_left) * math.cos(angle_right) / math.sin(angle_right))
        length_right = length_left * math.sin(angle_left) / math.sin(angle_right)

        return FinishedRegularPolygonFinishChamfer.__points_from_left_and_right_lengths(length_left,
                                                                                        length_right,
                                                                                        polygon)

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def __points_from_height_and_angle(height: float, angle: float, polygon: RegularPolygon) -> Tuple[Point2, Point2]:
        """
        Returns the intersection points of the chamfer and the two edges of the regular polygon given the height and
        the angle of the chamfer.

        :param height: The height of the chamfer.
        :param angle: The angle relative to the left edge of the regular polygon or the chamfer.
        :param polygon: The regular polygon.
        """
        angle_left = angle
        angle_right = math.pi - math.radians(polygon.inner_angle) - angle_left

        length_left = height / math.sin(angle_left)
        length_right = height / math.sin(angle_right)

        return FinishedRegularPolygonFinishChamfer.__points_from_left_and_right_lengths(length_left,
                                                                                        length_right,
                                                                                        polygon)

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def __points_from_left_and_right_lengths(length_left: float, length_right: float, polygon: RegularPolygon) -> Tuple[
        Point2, Point2]:
        """
        Returns the intersection points of the chamfer and the two edges of the regular polygon given the left and
        right lengths of the chamfer.

        :param length_left: The left length of the chamfer.
        :param length_right: The right length of the chamfer.
        :param polygon: The regular polygon.
        """
        alpha = 0.5 * math.radians(polygon.exterior_angle)
        point_left = Point2(-length_left * math.cos(alpha), -length_left * math.sin(alpha))
        point_right = Point2(length_right * math.cos(alpha), -length_right * math.sin(alpha))

        return point_left, point_right

    # ------------------------------------------------------------------------------------------------------------------
    def finishing(self, context: Context, polygon: RegularPolygon) -> ScadObject:
        """
        Returns an SuperSCAD object that will be subtracted from a node (a.k.a. corner) of a regular polygon. It is
        assumed that the node is located at the origin and is aligned along the y-axis.
        """
        if self.__length is not None:
            if self.__angle is None:
                angle: float = math.radians(0.5 * polygon.exterior_angle)
            else:
                angle = math.radians(self.__angle)
            point_left, point_right = self.__points_from_length_and_angle(self.__length, angle, polygon)

        elif self.__height is not None:
            if self.__angle is None:
                angle: float = math.radians(0.5 * polygon.exterior_angle)
            else:
                angle = math.radians(self.__angle)
            point_left, point_right = self.__points_from_height_and_angle(self.__height, angle, polygon)

        elif self.__left_length is not None:
            point_left, point_right = self.__points_from_left_and_right_lengths(self.__left_length,
                                                                                self.__right_length,
                                                                                polygon)

        else:
            point_left = Point2(0.0, 0.0)
            point_right = Point2(0.0, 0.0)

        length = math.sqrt((point_right.x - point_left.x) ** 2 + (point_right.y - point_left.y) ** 2)
        rotation = math.asin((point_right.y - point_left.y) / length)
        height = math.sqrt(point_left.x ** 2 + point_left.y ** 2) * math.cos(0.5 * math.radians(
                polygon.inner_angle) + rotation)

        return Translate2D(x=point_left.x,
                           y=point_left.y,
                           child=Rotate2D(angle=math.degrees(rotation),
                                          child=Translate2D(x=-context.eps,
                                                            child=Rectangle(width=length + 2.0 * context.eps,
                                                                            depth=height + context.eps))))

# ----------------------------------------------------------------------------------------------------------------------
