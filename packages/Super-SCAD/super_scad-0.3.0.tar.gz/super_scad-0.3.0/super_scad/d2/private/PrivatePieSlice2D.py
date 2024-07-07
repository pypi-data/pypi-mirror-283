import abc
import math

from super_scad.boolean.Difference import Difference
from super_scad.boolean.Empty import Empty
from super_scad.boolean.Intersection import Intersection
from super_scad.d2.Polygon import Polygon
from super_scad.scad.Context import Context
from super_scad.scad.ScadObject import ScadObject
from super_scad.type.Angle import Angle
from super_scad.type.Point2 import Point2


class PrivatePieSlice2D(ScadObject):
    """
    Abstract parent class for 2D pie slices.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def _validate_arguments(self) -> None:
        pass

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def angle(self) -> float:
        """
        Returns the angle of the pie slice.
        """
        return Angle.normalize(self.end_angle - self.start_angle)

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def start_angle(self) -> float:
        """
        Returns the start angle of the pie slice.
        """
        if 'angle' in self._args:
            return Angle.normalize(self._args['angle']) if self._args['angle'] < 0.0 else 0.0

        return Angle.normalize(self._args['start_angle'])

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def end_angle(self) -> float:
        """
        Returns the end angle of the pie slice.
        """
        if 'angle' in self._args:
            return Angle.normalize(self._args['angle']) if self._args['angle'] > 0.0 else 0.0

        return Angle.normalize(self._args['end_angle'])

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def radius(self) -> float:
        """
        Returns the outer radius of the pie slice.
        """
        return self.outer_radius

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def inner_radius(self) -> float:
        """
        Returns the inner radius of the pie slice.
        """
        return self.uc(self._args.get('inner_radius', 0.0))

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def outer_radius(self) -> float:
        """
        Returns the outer radius of the pie slice.
        """
        return self.uc(self._args.get('outer_radius', self._args.get('radius', 0.0)))

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def convexity(self) -> int:
        """
        Returns the convexity of the pie slice.
        """
        return 1 if self.angle < 180.0 else 2

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def __angular_to_vector(length: float, angle: float, ):
        return Point2(length * math.cos(math.radians(angle)), length * math.sin(math.radians(angle)))

    # ------------------------------------------------------------------------------------------------------------------
    @abc.abstractmethod
    def _create_circle(self, radius: float) -> ScadObject:
        """
        Creates a circle with given radius.

        :param radius: Radius of the circle.
        """
        raise NotImplementedError()

    # ------------------------------------------------------------------------------------------------------------------
    def build(self, context: Context) -> ScadObject:
        """
        Builds a SuperSCAD object.

        :param context: The build context.
        """
        angle = self.angle
        start_angle = self.start_angle
        end_angle = self.end_angle

        if self.outer_radius <= 0.0 or angle == 0.0:  # xxx Use rounding in target units.
            return Empty()

        if self.inner_radius == 0.0:  # xxx Use rounding in target units.
            circles = self._create_circle(self.outer_radius)
        else:
            circles = Difference(children=[self._create_circle(self.outer_radius),
                                           self._create_circle(self.inner_radius)])

        if round(angle - 360.0, 4) == 0.0:  # xxx Use rounding in target units.
            return circles

        if round(angle - 90.0, 4) < 0.0:  # xxx Use rounding in target units.
            size2 = (self.outer_radius + context.eps) / math.cos(math.radians(Angle.normalize(angle, 90.0) / 2.0))
            points = [Point2(0.0, 0.0),
                      self.__angular_to_vector(size2, start_angle),
                      self.__angular_to_vector(size2, end_angle)]

        elif round(angle - 90.0, 4) == 0.0:  # xxx Use rounding in target units.
            size1 = math.sqrt(2.0) * (self.outer_radius + context.eps)
            size2 = self.outer_radius + context.eps
            points = [Point2(0.0, 0.0),
                      self.__angular_to_vector(size2, start_angle),
                      self.__angular_to_vector(size1, start_angle + 45.0),
                      self.__angular_to_vector(size2, end_angle)]

        elif round(angle - 180.0, 4) == 0.0:  # xxx Use rounding in target units.
            size1 = math.sqrt(2.0) * (self.outer_radius + context.eps)
            size2 = self.outer_radius + context.eps
            points = [self.__angular_to_vector(size2, start_angle),
                      self.__angular_to_vector(size1, start_angle + 45.0),
                      self.__angular_to_vector(size1, start_angle + 135.0),
                      self.__angular_to_vector(size2, end_angle)]

        elif round(angle - 270.0, 4) == 0.0:  # xxx Use rounding in target units.
            size1 = math.sqrt(2.0) * (self.outer_radius + context.eps)
            size2 = self.outer_radius + context.eps
            points = [Point2(0.0, 0.0),
                      self.__angular_to_vector(size2, start_angle),
                      self.__angular_to_vector(size1, start_angle + 45.0),
                      self.__angular_to_vector(size1, start_angle + 135.0),
                      self.__angular_to_vector(size1, start_angle + 225.0),
                      self.__angular_to_vector(size2, end_angle)]

        elif round(angle - 180.0, 4) < 0.0:  # xxx Use rounding in target units.
            phi = Angle.normalize((start_angle - end_angle) / 2.0, 90.0)
            size1 = math.sqrt(2.0) * (self.outer_radius + context.eps)
            size2 = size1 / (math.cos(math.radians(phi)) + math.sin(math.radians(phi)))
            points = [Point2(0.0, 0.0),
                      self.__angular_to_vector(size2, start_angle),
                      self.__angular_to_vector(size1, start_angle - phi + 90.0),
                      self.__angular_to_vector(size1, start_angle - phi + 180.0),
                      self.__angular_to_vector(size2, end_angle)]

        elif round(angle - 360.0, 4) < 0.0:  # xxx Use rounding in target units.
            phi = Angle.normalize((start_angle - end_angle) / 2.0, 90.0)
            size1 = math.sqrt(2.0) * (self.outer_radius + context.eps)
            size2 = size1 / (math.cos(math.radians(phi)) + math.sin(math.radians(phi)))
            points = [Point2(0.0, 0.0),
                      self.__angular_to_vector(size2, start_angle),
                      self.__angular_to_vector(size1, start_angle - phi + 90.0),
                      self.__angular_to_vector(size1, start_angle - phi + 180.0),
                      self.__angular_to_vector(size1, start_angle - phi + 270.0),
                      self.__angular_to_vector(size2, end_angle)]

        else:
            raise ValueError('Math is broken!')

        return Intersection(children=[circles, Polygon(points=points, convexity=self.convexity)])

# ----------------------------------------------------------------------------------------------------------------------
