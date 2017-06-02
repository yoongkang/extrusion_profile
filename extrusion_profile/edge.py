import json
import math


class Vertex:
    """
    Represents a vertex
    """
    def __init__(self, id_, x, y):
        self.id = id_
        self.x = x
        self.y = y

    @classmethod
    def create_from_schema(cls, key, value):
        """Creates a Vertex based on a key-value pair from the schema"""
        position = value['Position']
        return cls(key, position['X'], position['Y'])


class Edge:
    """
    Base class for all Edge classes
    """
    VMAX = 0.5
    MACHINE_TIME_COST = 0.07

    def __init__(self, id_, vertices, *args):
        self.id = id_
        self.vertices = vertices

    @staticmethod
    def create_from_schema(key, value, all_vertices):
        """Creates an Edge based on a key-value pair from the schema"""
        class_type = edgefactory(value['Type'])
        vertices_for_edge = [all_vertices[str(k)] for k in value['Vertices']]
        return class_type._create_from_schema(key, value, vertices_for_edge)

    @classmethod
    def _create_from_schema(cls, key, value, vertices):
        raise NotImplementedError("Subclass should implement this method.")

    @property
    def cost(self):
        """Returns the cost of this Edge"""
        return self._cost

    @property
    def _cost(self):
        return 0

    @property
    def x_max(self):
        return 0

    @property
    def x_min(self):
        return 0

    @property
    def y_max(self):
        return 0

    @property
    def y_min(self):
        return 0


class LineSegmentEdge(Edge):
    """Represents a line segment edge"""

    @classmethod
    def _create_from_schema(cls, key, value, vertices):
        return cls(key, vertices)

    @property
    def _cost(self):
        horizontal_distance = self.vertices[0].x - self.vertices[1].x
        vertical_distance = self.vertices[0].y - self.vertices[1].y
        return (math.sqrt(horizontal_distance ** 2 + vertical_distance ** 2) / self.VMAX) * self.MACHINE_TIME_COST

    @property
    def x_max(self):
        return max([v.x for v in self.vertices])

    @property
    def x_min(self):
        return min([v.x for v in self.vertices])

    @property
    def y_max(self):
        return max([v.y for v in self.vertices])

    @property
    def y_min(self):
        return min([v.y for v in self.vertices])


def within(a, b, epsilon=1e6):
    """Returns True if number is within epsilon"""
    if abs(a - b) <= epsilon:
        return True
    return False


class CircularArcEdge(Edge):
    """Represents a circular arc edge"""
    def __init__(self, id_, vertices, center_x, center_y, clockwise_from):
        super().__init__(id_, vertices)
        self.center_x = center_x
        self.center_y = center_y
        self.clockwise_from = clockwise_from
        if self.clockwise_from == int(self.vertices[0].id):
            self.startpoint = self.vertices[0]
            self.endpoint = self.vertices[1]
        else:
            self.startpoint = self.vertices[1]
            self.endpoint = self.vertices[0]

    @classmethod
    def _create_from_schema(cls, key, value, vertices):
        return cls(key, vertices, value['Center']['X'], value['Center']['Y'], value['ClockwiseFrom'])

    @property
    def radius(self):
        return math.sqrt((self.center_x - self.startpoint.x) ** 2 + (self.center_y - self.startpoint.y) ** 2)

    def angle_at(self, x, y):
        angle = math.atan2(y - self.center_y, x - self.center_x)
        angle = (angle + 2 * math.pi) % (2 * math.pi)
        return angle

    @property
    def start_angle(self):
        return self.angle_at(self.startpoint.x, self.startpoint.y)

    @property
    def end_angle(self):
        return self.angle_at(self.endpoint.x, self.endpoint.y)

    @property
    def circumference(self):
        if self.end_angle > self.start_angle:
            return self.radius * (self.start_angle + (2 * math.pi - self.end_angle))
        return self.radius * (self.start_angle - self.end_angle)

    @property
    def _cost(self):
        speed = self.VMAX * math.exp(-1.0 / self.radius)
        return (self.circumference / speed) * self.MACHINE_TIME_COST

    def important_points(self):
        startpoint = (self.startpoint.x, self.startpoint.y)
        endpoint = (self.endpoint.x, self.endpoint.y)
        north = (self.center_x, self.center_y + self.radius)
        east = (self.center_x + self.radius, self.center_y)
        south = (self.center_x, self.center_y - self.radius)
        west = (self.center_x - self.radius, self.center_y)
        return startpoint, endpoint, north, east, south, west

    def point_in_arc(self, x, y):
        distance = math.sqrt((x - self.center_x) ** 2 + (y - self.center_y) ** 2)
        if within(distance, self.radius):
            angle = self.angle_at(x, y)
            if self.end_angle <= self.start_angle:
                return angle >= self.end_angle and angle <= self.start_angle
            return angle >= self.end_angle or angle <= self.start_angle
        return False

    @property
    def x_max(self):
        return max([x for x, y in self.important_points() if self.point_in_arc(x, y)])

    @property
    def x_min(self):
        return min([x for x, y in self.important_points() if self.point_in_arc(x, y)])

    @property
    def y_max(self):
        return max([y for x, y in self.important_points() if self.point_in_arc(x, y)])

    @property
    def y_min(self):
        return min([y for x, y in self.important_points() if self.point_in_arc(x, y)])


edge_mapping = {
    'LineSegment': LineSegmentEdge,
    'CircularArc': CircularArcEdge,
}

def edgefactory(edge_type):
    """Returns the Edge class given the edge_type"""
    return edge_mapping[edge_type]
